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

def compareAlliances(alliance1, alliance2, year, internet = "y"):

    utilityFunctions.clear()
    # print(f"{alliance1[0]}, {alliance1[1]}, {alliance1[2]} v.s {alliance2[0]}, {alliance2[1]}, {alliance2[2]}")
    # print(" ")

    # Load stats for every team in both alliances first, so we can find the
    # min/max of each stat across the whole group before rating anyone
    all_stats = {}
    for team in alliance1 + alliance2:
        if not os.path.exists(f"teamInfo/{team}.json"):
            print(f"Team {team} does not exist in teamInfo folder, pulling data from TBA...")
            if internet.lower() == "y":
                utilityFunctions.pullTeamData(team)
        with open(f"teamInfo/{team}.json", 'r') as file:
            data = json.load(file)
        # print(f"Reading season stats for team {team} {data['nickname']} from {year}")
        all_stats[team] = data['stats'][str(year)]

    mins, maxs = compute_min_max(list(all_stats.values()))

    utilityFunctions.clear()
    print(f"Alliance 1: {alliance1[0]}, {alliance1[1]}, {alliance1[2]}")
    for item in alliance1:
        print(f"Team {item}: {teamFunctions.printStats(all_stats[item])}\n")
    # for team, stats in alliance1.items():
    #     print(f"Team {team}: {teamFunctions.printStats(stats)}\n")

    print("")

    print(f"Alliance 2: {alliance2[0]}, {alliance2[1]}, {alliance2[2]}")
    for item in alliance2:
        print(f"Team {item}: {teamFunctions.printStats(all_stats[item])}\n")
    # for team, stats in alliance2.items():
    #     print(f"Team {team}: {teamFunctions.printStats(stats)}\n")
    
    print("")

    print("=" * 60)

    alliance1Score = sum(calculateRating(all_stats[team], mins, maxs) for team in alliance1)
    alliance2Score = sum(calculateRating(all_stats[team], mins, maxs) for team in alliance2)

    print(f"Alliance 1 rating: {alliance1Score:.2f}")
    print(f"Alliance 2 rating: {alliance2Score:.2f}")
    # print("")

    print("=" * 60)
    print(" ")

    if alliance1Score > alliance2Score:
        print("Alliance 1 predicted winner")
    elif alliance2Score > alliance1Score:
        print("Alliance 2 predicted winner")
    else:
        print("Predicted Tie")
    # utilityFunctions.#send_notification("Alliance analysis complete!")

def getAllianceDetails(alliance, year, internet = "y"):
    alliance_details = {}
    for team in alliance:
        if not os.path.exists(f"teamInfo/{team}.json"):
            print(f"Team {team} does not exist in teamInfo folder, pulling data from TBA...")
            if internet.lower() == "y":
                utilityFunctions.pullTeamData(team)
            else:
                print("You do not have an internet connection, so you cannot pull data for this team.")
                input("Press Enter to continue...")
                continue
        with open(f"teamInfo/{team}.json", 'r') as file:
            data = json.load(file)
        print(f"Reading season stats for team {team} {data['nickname']} from {year}")
        alliance_details[team] = data['stats'][str(year)]
    return alliance_details