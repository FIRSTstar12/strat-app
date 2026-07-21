import teamFunctions
import json

def calculateRating(stats):
    return (
        stats["win_percentage"] * 0.25 +
        stats["average_score"] * 0.20 +
        stats["longest_win_streak"] * 0.05 +
        stats["average_rp"] * 0.15 +
        stats["average_opr"] * 0.15
    )

def predictTeams(team1, team2, year):
    with open(f"teamInfo/{team1}.json", 'r') as file:
        data = json.load(file)
    team1Stats = data['stats'][str(year)]
    with open(f"teamInfo/{team2}.json", 'r') as file:
        info = json.load(file)
    team2Stats = info['stats'][str(year)]

    team1Rating = calculateRating(team1Stats)
    team2Rating = calculateRating(team2Stats)

    print(f"\n{team1} Rating: {team1Rating:.2f}")
    print(f"{team2} Rating: {team2Rating:.2f}")

    if team1Rating > team2Rating:
        return team1
    elif team2Rating > team1Rating:
        return team2
    else:
        return None

