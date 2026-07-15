import requests
import eventFunctions
import keys
from datetime import datetime
import utilityFunctions

currentYear = datetime.now().year

def getAverageRP(teamNumber, eventKey):
    rankings = requests.get(
        f"{keys.BASE_URL}/event/{eventKey}/rankings",
        headers=keys.headers
    ).json()

    for team in rankings["rankings"]:
        if team["team_key"] == f"frc{teamNumber}":
            return team["sort_orders"][0]

    return None

def getOPR(teamNumber, eventKey):
    oprs = requests.get(
        f"{keys.BASE_URL}/event/{eventKey}/oprs",
        headers=keys.headers
    ).json()

    return oprs["oprs"].get(f"frc{teamNumber}")

def getInfo(data):
    print(f"Team Name: {data['nickname']}")
    print(f"City: {data['city']}")
    print(f"Rookie Year: {data['rookie_year']}")

def getTeamMatches(team, year):
    url = f"https://www.thebluealliance.com/api/v3/team/frc{team}/matches/{year}"

    matches = requests.get(
        url,
        headers=keys.headers
    ).json()

    return matches

def calculateStats(teamNumber, year):
    team_matches = getTeamMatches(teamNumber, year)

    stats = {
        "matches": 0,
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "win_percentage": 0,
        "total_score": 0,
        "average_score": 0,
        "highest_score": 0,
        "lowest_score": float("inf"),
        "longest_win_streak": 0,
        "average_rp": 0,
        "average_opr": 0,
        "average_dpr": 0,
        "average_ccwm": 0,
        "events_attened": 0,
    }

    current_streak = 0
    events = eventFunctions.getTeamEvents(teamNumber, year)

    for match in team_matches:

        red_score = match["alliances"]["red"]["score"]
        blue_score = match["alliances"]["blue"]["score"]

        # Skip matches that haven't been played yet
        if red_score == -1 or blue_score == -1:
            continue

        red_teams = match["alliances"]["red"]["team_keys"]
        blue_teams = match["alliances"]["blue"]["team_keys"]

        if f"frc{teamNumber}" in red_teams:
            team_score = red_score
            opponent_score = blue_score

        elif f"frc{teamNumber}" in blue_teams:
            team_score = blue_score
            opponent_score = red_score

        else:
            continue

        stats["matches"] += 1
        stats["total_score"] += team_score

        stats["highest_score"] = max(stats["highest_score"], team_score)
        stats["lowest_score"] = min(stats["lowest_score"], team_score)

        

        for event in events:
            stats["average_rp"] += getAverageRP(teamNumber, event["key"])
            stats["average_opr"] += getOPR(teamNumber, year)
        stats["average_rp"] /= len(event)
        stats["average_opr"] /= len(event)

        if team_score > opponent_score:
            stats["wins"] += 1
            current_streak += 1
            stats["longest_win_streak"] = max(
                stats["longest_win_streak"],
                current_streak
            )

        elif team_score < opponent_score:
            stats["losses"] += 1
            current_streak = 0

        else:
            stats["ties"] += 1
            current_streak = 0

    if stats["matches"] > 0:
        stats["average_score"] = stats["total_score"] / stats["matches"]
        stats["win_percentage"] = (stats["wins"] / stats["matches"] * 100)
    else:
        stats["lowest_score"] = 0
        
    stats["events_attened"] = len(events)

    return stats

def printStats(stats):
    print("")
    print(f"Matches played: {stats['matches']}")
    print(f"Number of wins: {stats['wins']}")
    print(f"Number of losses: {stats['losses']}")
    print(f"Ties: {stats['ties']}")
    print(f"Win %: {stats['win_percentage']:.2f}%")
    print(f"Total Score: {stats['total_score']:.2f}")
    print(f"Average Score: {stats['average_score']:.2f}")
    print(f"Highest Score: {stats['highest_score']}")
    print(f"Lowest Score: {stats['lowest_score']:.2f}")
    print(f"Longest win streak: {stats['longest_win_streak']}")

def getTeam(teamNumber):
    response = requests.get(
        f"{keys.BASE_URL}/team/frc{teamNumber}",
        headers=keys.headers
    )

    if response.ok:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

def compareTeams(team1, team2, year):
    data = getTeam(team1)
    info = getTeam(team2)
    utilityFunctions.clear()
    print(f"Calculating season stats for team {team1} {data['nickname']} from {year}")
    team1Stats = calculateStats(team1, year)
    print(f"Calculating season stats for team {team2} {info['nickname']} from {year}")
    team2Stats = calculateStats(team2, year)

    utilityFunctions.clear()

    rating1 = calculateRating(team1Stats)
    rating2 = calculateRating(team2Stats)

    rows = [
        ("Matches", team1Stats['matches'], team2Stats['matches'], 0),
        ("Wins", team1Stats['wins'], team2Stats['wins'], 0),
        ("Losses", team1Stats['losses'], team2Stats['losses'], 0),
        ("Ties",team1Stats['ties'], team2Stats['ties'], 0),
        ("Win %", team1Stats['win_percentage'], team2Stats['win_percentage'], 1),
        ("Avg Score", team1Stats['average_score'], team2Stats['average_score'], 1),
        ("Highest Score", team1Stats['highest_score'], team2Stats['highest_score'], 1),
        ("Lowest Score", team1Stats['lowest_score'], team2Stats['lowest_score'], 1),
        ("Rating", rating1, rating2, 1),
    ]

    print("=" * 25)
    print(f"{'':<10}{team1:>7}{team2:>7}")
    print("-" * 25)
    for label, v1, v2, decimals in rows:
        print(f"{label:<10}{v1:>7.{decimals}f}{v2:>7.{decimals}f}")
    print("=" * 25)

def calculateRating(stats):
    rating = (
    stats["win_percentage"] * 0.25 +
    stats["average_score"] * 0.20 +
    stats["average_margin"] * 0.20 +
    stats["longest_win_streak"] * 0.05 +
    stats["average_rp"] * 0.15 +
    stats["opr"] * 0.15)
    return rating

def getTeamScore(match, teamNumber):
    red = match["alliances"]["red"]
    blue = match["alliances"]["blue"]

    if f"frc{teamNumber}" in red["team_keys"]:
        return red["score"], blue["score"]

    if f"frc{teamNumber}" in blue["team_keys"]:
        return blue["score"], red["score"]

    return None, None