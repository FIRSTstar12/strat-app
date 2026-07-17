# Main Program
from datetime import datetime
import os
from utilityFunctions import clear, get_team_numbers, getLastUpdatedYear, intro, pullTeamData, send_notification
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
# print(teamFunctions.eventStats(1619,"2026code"))

if os.path.exists("teamInfo") == False:
    found = input("No teamInfo folder found, would you like to create one? (y/n): ")
    if found == "y":
        os.mkdir("teamInfo")
        print("teamInfo folder created")
while True:
    clear()
    choice = options()

    if keyboard.is_pressed('q'):
        clear()
        print("Quitting...")
        exit()

    if choice == 10:
        clear()
        print("Exiting...")
        clear()
        break

    if choice < 1 or choice > 10:
        clear()
        print("Invalid choice")
        input("Press Enter to continue...")
        continue

    if choice <= 4:
        clear()
        teamNumber = int(input("What team do you want to look for?: "))

        if choice == 1:  # Gets data for one team in one season
            year = int(input("What year would you like to look at?: "))
            clear()
            data = getTeam(teamNumber)
            print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
            stats = calculateStats(teamNumber, year)
            printStats(stats)

        elif choice == 2:  # Gets data for team's lifetime
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
            send_notification("Lifetime Stat Search Complete")

        elif choice == 3:  # Compares two teams
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            year = int(input("What year would you like to look at?: "))
            clear()
            compareTeams(teamNumber, otherTeam, year)

        elif choice == 4:  # Predicts who would win between two teams
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            year = int(input("What year would you like to look at?: "))
            clear()
            winner = predictTeams(teamNumber, otherTeam, year)
            if winner is None:
                print("Predicted Tie")
            else:
                print(f"Predicted Winner: {winner}")
            send_notification("Prediction Complete")

    else:
        if choice == 5:  # predicts alliance
            currentYear = datetime.now().year
            compareAlliances(buildAlliance(), buildAlliance(), currentYear)
        elif choice == 6:  # prints match info
            matchCode = input("Please enter the match code: ")
            print(getMatchInfo(matchCode))
        elif choice == 7:  # prints event info
            eventCode = input("Please enter the event code: ")
            getEventInfo(eventCode)
        elif choice == 8:  # pulls new team data from TBA
            teamNumber = int(input("Please enter the team number: "))
            pullTeamData(teamNumber)
        elif choice == 9:  # pulls new team data for multiple teams from TBA
            teamNumbers = input("Please enter the team numbers separated by commas: ")
            teamNumbers = [int(x.strip()) for x in teamNumbers.split(",")]
            currentNums = get_team_numbers("teamInfo")
            for teamNumber in teamNumbers:
                update = getLastUpdatedYear(teamNumber)
                if teamNumber in currentNums and os.path.exists(f"teamInfo/{teamNumber}.json") and update is not None and update >= datetime.now().year:
                    # send_notification(f"Team {teamNumber} already exists in teamInfo folder, skipping...")
                    teamNumbers.remove(teamNumber)
            send_notification(f"Pulling data for teams: {teamNumbers}")
            for teamNumber in teamNumbers:
                pullTeamData(teamNumber)
            send_notification(f"Data has been collected for {teamNumbers}")

    input("Press Enter to continue...")