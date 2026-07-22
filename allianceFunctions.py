import os
import json
from predictionFunctions import calculateRating, compute_min_max
import teamFunctions
import utilityFunctions

def buildAlliance():
    team1 = int(input("Enter in the first team number: "))
    team2 = int(input("Enter in the second team number: "))
    team3 = int(input("Enter in the third team number: "))
    return [team1,team2,team3]

def compareAlliances(alliance1, alliance2, year):

    utilityFunctions.clear()
    print(f"{alliance1[0]}, {alliance1[1]}, {alliance1[2]} v.s {alliance2[0]}, {alliance2[1]}, {alliance2[2]}")
    print(" ")

    # Load stats for every team in both alliances first, so we can find the
    # min/max of each stat across the whole group before rating anyone
    all_stats = {}
    for team in alliance1 + alliance2:
        if not os.path.exists(f"teamInfo/{team}.json"):
            print(f"Team {team} does not exist in teamInfo folder, pulling data from TBA...")
            utilityFunctions.pullTeamData(team)
        with open(f"teamInfo/{team}.json", 'r') as file:
            data = json.load(file)
        print(f"Reading season stats for team {team} {data['nickname']} from {year}")
        all_stats[team] = data['stats'][str(year)]

    mins, maxs = compute_min_max(list(all_stats.values()))

    print("")

    alliance1Score = sum(calculateRating(all_stats[team], mins, maxs) for team in alliance1)
    alliance2Score = sum(calculateRating(all_stats[team], mins, maxs) for team in alliance2)

    print(f"Alliance 1 rating: {alliance1Score:.2f}")
    print(f"Alliance 2 rating: {alliance2Score:.2f}")
    print("")

    if alliance1Score > alliance2Score:
        print("Alliance 1 predicted winner")
    elif alliance2Score > alliance1Score:
        print("Alliance 2 predicted winner")
    else:
        print("Predicted Tie")
    utilityFunctions.send_notification("Alliance analysis complete!")