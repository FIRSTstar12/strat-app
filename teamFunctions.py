import requests
import eventFunctions
import keys
from datetime import datetime
import utilityFunctions

currentYear = datetime.now().year

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
        "total_score": 0
    }

    for match in team_matches:
        info = eventFunctions.getMatchInfo(match["key"])

        red_score = info["alliances"]["red"]["score"]
        blue_score = info["alliances"]["blue"]["score"]

        red_teams = info["alliances"]["red"]["team_keys"]
        blue_teams = info["alliances"]["blue"]["team_keys"]

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

        if team_score > opponent_score:
            stats["wins"] += 1
        elif team_score < opponent_score:
            stats["losses"] += 1
        else:
            stats["ties"] += 1

    if stats["matches"] > 0:
        stats["average_score"] = stats["total_score"] / stats["matches"]
        stats["win_percentage"] = stats["wins"] / stats["matches"] * 100
    else:
        stats["average_score"] = 0
        stats["win_percentage"] = 0

    return stats

def printStats(stats):
    print("")
    print(f"Matches played: {stats['matches']}")
    print(f"Number of wins: {stats['wins']}")
    print(f"Number of losses: {stats['losses']}")
    print(f"Ties: {stats['ties']}")
    print(f"Win %: {stats['win_percentage']:.2f}%")
    print(f"Average Score: {stats['average_score']:.2f}")

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
    print(f"Calculating season stats for team {team1} {data['nickname']} from {year}")
    team1Stats = calculateStats(team1, year)
    print(f"Calculating season stats for team {team2} {info['nickname']} from {year}")
    team2Stats = calculateStats(team2, year)

    print(f"\nComparing {team1} vs {team2}")
    print("----------------------------")

    print(f"{team1} Average Score: {team1Stats['average_score']:.2f}")
    print(f"{team2} Average Score: {team2Stats['average_score']:.2f}")

    print(f"{team1} Win %: {team1Stats['win_percentage']:.2f}%")
    print(f"{team2} Win %: {team2Stats['win_percentage']:.2f}%")

def calculateRating(stats):
    return (
        stats["average_score"] * 0.6 +
        stats["win_percentage"] * 0.4
    )

def predictTeams(team1, team2, year):
    team1Stats = calculateStats(team1, year)
    team2Stats = calculateStats(team2, year)

    team1Rating = calculateRating(team1Stats)
    team2Rating = calculateRating(team2Stats)

    print(f"\n{team1} Rating: {team1Rating:.2f}")
    print(f"{team2} Rating: {team2Rating:.2f}")

    if team1Rating > team2Rating:
        print(f"Prediction: Team {team1} wins")
    elif team2Rating > team1Rating:
        print(f"Prediction: Team {team2} wins")
    else:
        print("Prediction: Tie")