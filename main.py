# Main Program
from datetime import datetime
import utilityFunctions
import teamFunctions
import eventFunctions
import predictionFunctions

utilityFunctions.clear()
choice = utilityFunctions.options()
utilityFunctions.clear()

if choice > 6:
    print("Invalid choice")

if choice < 5:
    teamNumber = int(input("What team do you want to look for?: "))

    if choice == 1:  #Gets data for one team in one season
        year = int(input("What year would you like to look at?: "))
        utilityFunctions.clear()
        data = teamFunctions.getTeam(teamNumber)
        print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
        stats = teamFunctions.calculateStats(teamNumber, year)
        teamFunctions.printStats(stats)

    elif choice == 2: #Gets data for team's lifetime
        year = int(input("What year would you like to look at?: "))
        utilityFunctions.clear()
        data = teamFunctions.getTeam(teamNumber)
        currentYear = datetime.now().year
        year = data['rookie_year']
        while year != currentYear:
            print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
            stats = teamFunctions.calculateStats(teamNumber, year)
            teamFunctions.printStats(stats)
            year += 1
            print(" ")

    elif choice == 3: #Compares two teams
        otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
        year = int(input("What year would you like to look at?: "))
        teamFunctions.compareTeams(teamNumber,otherTeam,year)
    
    elif choice == 4: #Predicts who would win between two teams
        otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
        year = int(input("What year would you like to look at?: "))
        utilityFunctions.clear()
        predictionFunctions.predictTeams(teamNumber,otherTeam,year)
    else:
        if choice == 5: #prints match info
            matchCode = input("Please enter the match code: ")
            print(eventFunctions.getMatchInfo(matchCode))
        elif choice == 6: #prints event info
            eventCode = input("Please enter the event code: ")
            eventFunctions.getEventInfo(eventCode)
        else:
            print("Invalid Choice")
