from predictionFunctions import calculateRating
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

    alliance1Score = 0
    alliance2Score = 0

    for team in alliance1:
        data = teamFunctions.getTeam(team)
        print(f"Calculating season stats for team {team} {data['nickname']} from {year}")
        stats = teamFunctions.calculateStats(team, year)
        alliance1Score += calculateRating(stats)
    
    print("")

    for team in alliance2:
        info = teamFunctions.getTeam(team)
        print(f"Calculating season stats for team {team} {info['nickname']} from {year}")
        stats = teamFunctions.calculateStats(team, year)
        alliance2Score += calculateRating(stats)

    print("")
    print(f"Alliance 1 rating: {alliance1Score:.2f}")
    print(f"Alliance 2 rating: {alliance2Score:.2f}")
    print("")

    if alliance1Score > alliance2Score:
        print("Alliance 1 predicted winner")
    else:
        print("Alliance 2 predicted winner")