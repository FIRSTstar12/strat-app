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

def findBestAlliance(teams, year):
    bestAlliance = None
    bestRating = 0

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            for k in range(j + 1, len(teams)):
                alliance = [teams[i], teams[j], teams[k]]
                rating = 0
                for team in alliance:
                    with open(f"teamInfo/{team}.json", 'r') as file:
                        data = json.load(file)
                    teamStats = data['stats'][str(year)]
                    rating += calculateRating(teamStats)

                if rating > bestRating:
                    bestRating = rating
                    bestAlliance = alliance
                    print(f"Current Best Alliance: {bestAlliance}, Rating: {bestRating:.2f}\n")
                
                print(f"Alliance: {alliance}, Rating: {rating:.2f}\n")
                

    return bestAlliance, bestRating