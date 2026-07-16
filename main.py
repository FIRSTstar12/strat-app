# Main Program
from datetime import datetime
from utilityFunctions import clear, intro, pullTeamData
from teamFunctions import getTeam
from teamFunctions import calculateStats    
from teamFunctions import printStats
from teamFunctions import compareTeams
from predictionFunctions import predictTeams
from allianceFunctions import compareAlliances, buildAlliance
from utilityFunctions import options
from eventFunctions import getMatchInfo, getEventInfo
import keyboard

clear()
intro()
# print(teamFunctions.eventStats(1619,"2026code"))\
choice = options()
clear()
while choice != 10:
    if keyboard.is_pressed('q'):
        print("Quiting...")
        exit()
    if choice > 10 or choice < 1:
        print("Invalid choice")

    if choice < 5:
        teamNumber = int(input("What team do you want to look for?: "))

        if choice == 1:  #Gets data for one team in one season
            year = int(input("What year would you like to look at?: "))
            clear()
            data = getTeam(teamNumber)
            print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
            stats = calculateStats(teamNumber, year)
            printStats(stats)

        elif choice == 2: #Gets data for team's lifetime
            year = int(input("What year would you like to look at?: "))
            clear()
            data = getTeam(teamNumber)
            currentYear = datetime.now().year
            year = data['rookie_year']
            while year != currentYear:
                print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
                stats = calculateStats(teamNumber, year)
                printStats(stats)
                year += 1
                print(" ")

        elif choice == 3: #Compares two teams
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            year = int(input("What year would you like to look at?: "))
            clear()
            compareTeams(teamNumber,otherTeam,year)
    
        elif choice == 4: #Predicts who would win between two teams
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            year = int(input("What year would you like to look at?: "))
            clear()
            winner = predictTeams(teamNumber,otherTeam,year)
            if winner is None:
                print("Predicted Tie")
            else:
                print(f"Predicted Winner: {winner}")
    
    else:
        if choice == 5: #predicts alliance 
            currentYear = datetime.now().year
            compareAlliances(buildAlliance(),buildAlliance(),currentYear)
        elif choice == 6: #prints match info
            matchCode = input("Please enter the match code: ")
            print(getMatchInfo(matchCode))
        elif choice == 7: #prints event info
            eventCode = input("Please enter the event code: ")
            getEventInfo(eventCode)
        elif choice == 8: #pulls new team data from TBA
            teamNumber = int(input("Please enter the team number: "))
            pullTeamData(teamNumber)
        elif choice == 9: #pulls new team data for multiple teams from TBA
            teamNumbers = input("Please enter the team numbers separated by commas: ")
            teamNumbers = [int(x.strip()) for x in teamNumbers.split(",")]
            for teamNumber in teamNumbers:
                pullTeamData(teamNumber)
        elif choice == 10:
            print("Exiting...")
            exit()
        else:
            print("Invalid Choice")