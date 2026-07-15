import teamFunctions

def calculateRating(stats):
    return (
        stats["average_score"] * 0.6 +
        stats["win_percentage"] * 0.4
    )

def predictTeams(team1, team2, year):
    team1Stats = teamFunctions.calculateStats(team1, year)
    team2Stats = teamFunctions.calculateStats(team2, year)

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