import requests
import eventFunctions
import keys
from datetime import datetime
import utilityFunctions
from predictionFunctions import calculateRating

currentYear = datetime.now().year

def eventStats(teamNumber, eventKey):
    rankings = requests.get(
        f"{keys.BASE_URL}/event/{eventKey}/rankings",
        headers=keys.headers
    ).json()

    for team in rankings["rankings"]:
        if team["team_key"] == f"frc{teamNumber}":
            return {
                "average_rp": team["sort_orders"][0],
                "rank": team["rank"]
            }

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

def addEventStats(stats, teamNumber, year):
    events = eventFunctions.getTeamEvents(teamNumber, year)

    stats["events_attended"] = len(events)

    for event in events:
        event_data = eventStats(teamNumber, event["key"])
        opr = getOPR(teamNumber, event["key"])

        if event_data:
            stats["average_rp"] += event_data["average_rp"]
            stats["average_rank"] += event_data["rank"]

        if opr is not None:
            stats["average_opr"] += opr

    if events:
        stats["average_rp"] /= len(events)
        stats["average_rank"] /= len(events)
        stats["average_opr"] /= len(events)

def calculateStats(teamNumber, year):
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
        "events_attended": 0,
        "average_rank": 0,
    }
    team_matches = getTeamMatches(teamNumber, year)

    current_streak = 0

    for match in team_matches:

        red_score = match["alliances"]["red"]["score"]
        blue_score = match["alliances"]["blue"]["score"]

        if red_score == -1 or blue_score == -1:
            continue

        team_score, opponent_score = getTeamScore(match, teamNumber)

        if team_score is None:
            continue

        stats["matches"] += 1
        stats["total_score"] += team_score

        stats["highest_score"] = max(stats["highest_score"], team_score)
        stats["lowest_score"] = min(stats["lowest_score"], team_score)


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
    
    addEventStats(stats, teamNumber, year)

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

def getTeamScore(match, teamNumber):
    red = match["alliances"]["red"]
    blue = match["alliances"]["blue"]

    if f"frc{teamNumber}" in red["team_keys"]:
        return red["score"], blue["score"]

    if f"frc{teamNumber}" in blue["team_keys"]:
        return blue["score"], red["score"]

    return None, None
