from predictionFunctions import calculateRating
import teamFunctions

def compareAlliances(alliance1, alliance2, year):

    alliance1Score = 0
    alliance2Score = 0

    for team in alliance1:
        stats = teamFunctions.calculateStats(team, year)
        alliance1Score += calculateRating(stats)

    for team in alliance2:
        stats = teamFunctions.calculateStats(team, year)
        alliance2Score += calculateRating(stats)

    print(f"Alliance 1 rating: {alliance1Score:.2f}")
    print(f"Alliance 2 rating: {alliance2Score:.2f}")

    if alliance1Score > alliance2Score:
        print("Alliance 1 predicted winner")
    else:
        print("Alliance 2 predicted winner")