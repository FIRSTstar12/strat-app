import io
import os
import json
import contextlib
from datetime import datetime

import discord
from discord.ext import commands

from keys import TOKEN
import utilityFunctions
from teamFunctions import getTeam, calculateStats, printStats, compareTeams
from predictionFunctions import predictTeams, findBestAlliance
from eventFunctions import getMatchInfo, getEventInfo, getEventTeams

intents = discord.Intents.default()
intents.message_content = True  # required so the bot can read "!" command text

bot = commands.Bot(command_prefix="!", intents=intents)


def capture(func, *args, **kwargs):
    """Run a function that normally prints to the console and return
    whatever it printed, so it can be sent back as a Discord message."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result = func(*args, **kwargs)
    return buf.getvalue(), result


async def send_long(ctx, text: str):
    """Discord messages are capped at 2000 characters, so split long
    console output (like printStats/compareTeams) into chunks."""
    text = text.strip() or "(no output)"
    for i in range(0, len(text), 1900):
        await ctx.send(f"```{text[i:i + 1900]}```")


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="stats")
async def stats_cmd(ctx, team: int, year: int = None):
    """!stats <team> [year] - season stats for a team (defaults to current year)."""
    year = year or datetime.now().year
    async with ctx.typing():
        path = f"teamInfo/{team}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            stats = data.get("stats", {}).get(str(year))
            if stats is None:
                await ctx.send(f"No saved stats for team {team} in {year}. Try `!pull {team}` first.")
                return
        else:
            data = getTeam(team)
            if data is None:
                await ctx.send(f"Could not find team {team} on The Blue Alliance.")
                return
            stats = calculateStats(team, year)

        output, _ = capture(printStats, stats)
        await ctx.send(f"**Team {team} — {data.get('nickname', 'Unknown')} ({year})**")
        await send_long(ctx, output)


@bot.command(name="compare")
async def compare_cmd(ctx, team1: int, team2: int, year: int = None):
    """!compare <team1> <team2> [year] - side-by-side comparison of two teams."""
    year = year or datetime.now().year
    async with ctx.typing():
        for t in (team1, team2):
            if not os.path.exists(f"teamInfo/{t}.json"):
                utilityFunctions.pullTeamData(t)
        output, _ = capture(compareTeams, team1, team2, year)
        await send_long(ctx, output)


@bot.command(name="predict")
async def predict_cmd(ctx, team1: int, team2: int, year: int = None):
    """!predict <team1> <team2> [year] - predicted winner between two teams."""
    year = year or datetime.now().year
    async with ctx.typing():
        for t in (team1, team2):
            if not os.path.exists(f"teamInfo/{t}.json"):
                utilityFunctions.pullTeamData(t)
        output, winner = capture(predictTeams, team1, team2, year)
        await send_long(ctx, output)
        if winner is None:
            await ctx.send("Predicted result: **Tie**")
        else:
            await ctx.send(f"Predicted winner: **Team {winner}**")


@bot.command(name="alliance")
async def alliance_cmd(ctx, *, teams: str):
    """!alliance 254,1114,118,2056 - best 3-team alliance from a comma-separated list."""
    year = datetime.now().year
    team_numbers = [int(t.strip()) for t in teams.split(",") if t.strip()]
    async with ctx.typing():
        for t in team_numbers:
            if not os.path.exists(f"teamInfo/{t}.json"):
                utilityFunctions.pullTeamData(t)
        output, (best, rating) = capture(findBestAlliance, team_numbers, year)
        if best is None:
            await ctx.send("Could not determine a best alliance from that list.")
        else:
            await ctx.send(f"Best alliance: **{best}** — rating {rating:.2f}")


@bot.command(name="match")
async def match_cmd(ctx, match_code: str):
    """!match 2024casj_qm1 - raw match info by TBA match code."""
    async with ctx.typing():
        info = getMatchInfo(match_code)
        await send_long(ctx, json.dumps(info, indent=2))


@bot.command(name="event")
async def event_cmd(ctx, event_code: str):
    """!event 2024casj - match list for an event code."""
    async with ctx.typing():
        output, _ = capture(getEventInfo, event_code)
        await send_long(ctx, output)


@bot.command(name="pull")
async def pull_cmd(ctx, team: int):
    """!pull <team> - fetch/refresh a team's data from The Blue Alliance."""
    async with ctx.typing():
        utilityFunctions.pullTeamData(team)
        await ctx.send(f"Data pulled and saved for team {team}.")


if __name__ == "__main__":
    if not os.path.exists("teamInfo"):
        os.mkdir("teamInfo")
    bot.run(TOKEN)