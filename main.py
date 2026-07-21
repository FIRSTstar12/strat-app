# Main Program
from datetime import datetime
import os
from utilityFunctions import clear, get_team_numbers, getLastUpdatedYear, intro, pullTeamData, send_notification
from teamFunctions import getTeam, pullMultipleTeamData
from teamFunctions import calculateStats    
from teamFunctions import printStats
from teamFunctions import compareTeams
from predictionFunctions import predictTeams
from allianceFunctions import compareAlliances, buildAlliance
from utilityFunctions import options
from eventFunctions import getEventTeams, getMatchInfo, getEventInfo
import keyboard
import json

clear()
intro()

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
            if not os.path.exists(f"teamInfo/{teamNumber}.json"):
                data = getTeam(teamNumber)
                print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
                stats = calculateStats(teamNumber, year)
                printStats(stats)
            else:
                with open(f"teamInfo/{teamNumber}.json", 'r') as file:
                    data = json.load(file)
                # data = getTeam(teamNumber)
                print(f"Reading season stats for team {teamNumber} {data['nickname']} from {year}")
                stats = data['stats'][str(year)]
                printStats(stats)

        elif choice == 2:  # Gets data for team's lifetime
            clear()
            if not os.path.exists(f"teamInfo/{teamNumber}.json"):
                print(f"Team {teamNumber} does not exist in teamInfo folder, pulling data from TBA...")
                pullTeamData(teamNumber)
            with open(f"teamInfo/{teamNumber}.json", 'r') as file:
                    data = json.load(file)
            
            currentYear = datetime.now().year
            year = data['rookie_year']
            while year != currentYear:
                # print(f"Calculating season stats for team {teamNumber} {data['nickname']} from {year}")
                stats = data['stats'][str(year)]
                printStats(stats)
                year += 1
                print(" ")
            send_notification(f"Lifetime Stat Search Complete for team {teamNumber} {data['nickname']}")

        elif choice == 3:  # Compares two teams
            if not os.path.exists(f"teamInfo/{teamNumber}.json"):
                print(f"Team {teamNumber} does not exist in teamInfo folder, pulling data from TBA...")
                pullTeamData(teamNumber)
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            if not os.path.exists(f"teamInfo/{otherTeam}.json"):
                print(f"Team {otherTeam} does not exist in teamInfo folder, pulling data from TBA...")
                pullTeamData(otherTeam)
            year = int(input("What year would you like to look at?: "))
            clear()
            compareTeams(teamNumber, otherTeam, year)

        elif choice == 4:  # Predicts who would win between two teams
            if not os.path.exists(f"teamInfo/{teamNumber}.json"):
                print(f"Team {teamNumber} does not exist in teamInfo folder, pulling data from TBA...")
                pullTeamData(teamNumber)
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            if not os.path.exists(f"teamInfo/{otherTeam}.json"):
                print(f"Team {otherTeam} does not exist in teamInfo folder, pulling data from TBA...")
                pullTeamData(otherTeam)
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
            manualOrAuto = input("Would you like to enter the team numbers manually or automatically? (m/a): ")
            if manualOrAuto.lower() == "m":
                pullMultipleTeamData()
            else:
                clear()
                eventCode = input("Please enter the event code: ")
                teams = getEventTeams(eventCode)
                send_notification(f"Pulling data for {len(teams)} teams from {eventCode}")
                teamsDone = 0
                for team in teams:
                    pullTeamData(team)
                    teamsDone += 1
                    send_notification(f"Data has been collected for {teamsDone}/{len(teams)} teams from {eventCode}")
                    clear()
                send_notification(f"Data collection complete for {len(teams)} teams from {eventCode}")
                print(f"Data collection complete for {len(teams)} teams from {eventCode}")
                break
    input("Press Enter to continue...")