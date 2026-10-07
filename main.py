from datetime import datetime
import os
from utilityFunctions import clear, get_team_numbers, getLastUpdatedYear, intro, pullTeamData#send_notifcation
from teamFunctions import getTeam, pullMultipleTeamData
from teamFunctions import calculateStats    
from teamFunctions import printStats
from teamFunctions import compareTeams
from predictionFunctions import getTopThreeAlliances, predictTeams, findBestAlliance
from allianceFunctions import compareAlliances, buildAlliance, getAllianceDetails
from utilityFunctions import options
from eventFunctions import getEventTeams, getMatchInfo, getEventInfo
from readingData import data, getEvents
import keyboard
import json

clear()
intro()
internet = input("Do you have an internet connection? (y/n): ")
if internet.lower() == "n":
    print("You will not be able to pull new data from TBA, but you can still use the program with existing data.")
repull = input("Would you like to repull all team data from TBA? (y/n): ")

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

    if choice == 13 or choice == 14:
        clear()
        print("Exiting...")
        clear()
        break

    if choice < 1 or choice > 14:
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
            #send_notifcation(f"Lifetime Stat Search Complete for team {teamNumber} {data['nickname']}")

        elif choice == 3:  # Compares two teams
            if not os.path.exists(f"teamInfo/{teamNumber}.json"):
                print(f"Team {teamNumber} does not exist in teamInfo folder, pulling data from TBA...")
                if internet.lower() == "y":
                    pullTeamData(teamNumber)
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            if not os.path.exists(f"teamInfo/{otherTeam}.json"):
                print(f"Team {otherTeam} does not exist in teamInfo folder, pulling data from TBA...")
                if internet.lower() == "y":
                    pullTeamData(otherTeam)
                else:
                    print("You do not have an internet connection, so you cannot pull data for this team.")
                    input("Press Enter to continue...")
                    continue
            year = int(input("What year would you like to look at?: "))
            clear()
            compareTeams(teamNumber, otherTeam, year)

        elif choice == 4:  # Predicts who would win between two teams
            if not os.path.exists(f"teamInfo/{teamNumber}.json"):
                print(f"Team {teamNumber} does not exist in teamInfo folder, pulling data from TBA...")
                if internet.lower() == "y":
                    pullTeamData(teamNumber)
            otherTeam = int(input(f"What team do you want to compare to {teamNumber}?: "))
            if not os.path.exists(f"teamInfo/{otherTeam}.json"):
                print(f"Team {otherTeam} does not exist in teamInfo folder, pulling data from TBA...")
                if internet.lower() == "y":
                    pullTeamData(otherTeam)
                else:
                    print("You do not have an internet connection, so you cannot pull data for this team.")
                    input("Press Enter to continue...")
                    continue
            year = int(input("What year would you like to look at?: "))
            clear()
            winner = predictTeams(teamNumber, otherTeam, year)
            if winner is None:
                print("Predicted Tie")
            else:
                print(f"Predicted Winner: {winner}")
            #send_notifcation("Prediction Complete")

    else:
        if choice == 5:  # predicts alliance
            currentYear = datetime.now().year
            compareAlliances(buildAlliance(), buildAlliance(), currentYear)
        elif choice == 6:  # prints match info
            if not internet.lower() == "y":
                print("You do not have an internet connection, so you cannot pull match data.")
                input("Press Enter to continue...")
                continue
            matchCode = input("Please enter the match code: ")
            print(getMatchInfo(matchCode))
        elif choice == 7:  # prints event info
            if not internet.lower() == "y":
                print("You do not have an internet connection, so you cannot pull event data.")
                input("Press Enter to continue...")
                continue
            eventCode = input("Please enter the event code: ")
            getEventInfo(eventCode)
        elif choice == 8:  # pulls new team data from TBA
            if not internet.lower() == "y":
                print("You do not have an internet connection, so you cannot pull team data.")
                input("Press Enter to continue...")
                continue
            teamNumber = int(input("Please enter the team number: "))
            pullTeamData(teamNumber)
        elif choice == 9:  # pulls new team data for multiple teams from TBA
            manualOrAuto = input("Would you like to enter the team numbers manually or automatically? (m/a): ")
            if manualOrAuto.lower() == "m":
                teamNumbers = [int(x.strip()) for x in input("Please enter the team numbers separated by commas: ").split(",")]
                if not internet.lower() == "y":
                    print("You do not have an internet connection, so you cannot pull team data.")
                    input("Press Enter to continue...")
                    continue
                pullMultipleTeamData(teamNumbers)
            else:
                clear()
                eventCode = input("Please enter the event code: ")
                teams = getEventTeams(eventCode)
                #send_notifcation(f"Pulling data for {len(teams)} teams from {eventCode}")
                teamsDone = 0
                if not internet.lower() == "y":
                    print("You do not have an internet connection, so you cannot pull team data.")
                    input("Press Enter to continue...")
                    continue
                for team in teams:
                    pullTeamData(team)
                    teamsDone += 1
                    #send_notifcation(f"Data has been collected for {teamsDone}/{len(teams)} teams from {eventCode}")
                    clear()
                #send_notifcation(f"Data collection complete for {len(teams)} teams from {eventCode}")
                print(f"Data collection complete for {len(teams)} teams from {eventCode}")
                break
        elif choice == 10:  # finds best alliance for a set of teams
            clear()
            manualOrAuto = input("Would you like to enter the team numbers manually or automatically? (m/a): ")
            if manualOrAuto.lower() == "m":
                teamNumbers = []
                while True:
                    teamNumber = input("Please enter a team number (or type 'done' to finish): ")
                    if teamNumber.lower() == 'done':
                        break
                    elif teamNumber.isdigit():
                        teamNumbers.append(int(teamNumber))
                    else:
                        print("Invalid input. Please enter a valid team number or 'done'.")
            else:
                clear()
                if not internet.lower() == "y":
                    print("You do not have an internet connection, so you cannot pull team data.")
                    input("Press Enter to continue...")
                    continue
                eventCode = input("Please enter the event code: ")
                teamNumbers = getEventTeams(eventCode)
                if repull.lower() == "y":
                    # pullMultipleTeamData(teamNumbers)
                    #send_notifcation(f"Pulling data for {len(teamNumbers)} teams from {eventCode}")
                    teamsDone = 0
                    for team in teamNumbers:
                    # if not os.path.exists(f"teamInfo/{team}.json") or getLastUpdatedYear(team) < datetime.now():
                        pullTeamData(team)
                        teamsDone += 1
                        #send_notifcation(f"Data has been collected for {teamsDone}/{len(teamNumbers)} teams from {eventCode}")
                        clear()
                    # #send_notifcation(f"Data collection complete for {len(teamNumbers)} teams from {eventCode}")
                        print(f"Data collection complete for {teamsDone}/{len(teamNumbers)} teams from {eventCode}")
            currentYear = datetime.now().year
            # bestAlliance, bestRating = findBestAlliance(teamNumbers, currentYear)
            topThreeAlliances = getTopThreeAlliances(teamNumbers, currentYear)
            print("\nTop Three Alliances:")
            for i, (alliance, rating) in enumerate(topThreeAlliances, start=1):
                print(f"{i}. Alliance: {alliance}, Rating: {rating:.2f}\n")
                alliance_details = getAllianceDetails(alliance, currentYear)
                print("Alliance Details:")
                for team, stats in alliance_details.items():
                    print(f"Team {team}: {printStats(stats)}\n")
            # print(f"Best Alliance: {bestAlliance} with a rating of {bestRating:.2f}")
            # #send_notifcation("Best Alliance Prediction Complete")
            # #send_notifcation(f"Best Alliance: {bestAlliance} with a rating of {bestRating:.2f}")
        elif choice == 11: 
            clear()
            for team in data:
                print(team)
            # clear()
            break
        elif choice == 12:
            print("This option is not available yet, but it will be in the future.")
            # clear()
            # centerTeam = int(input("Enter the team that must be on this Alliance: "))
            # eventCode = input("Please enter the event code: ")
            # teamNumbers = getEventTeams(eventCode)
            # # #send_notifcation(f"Pulling data for {len(teamNumbers)} teams from {eventCode}")
            # teamsDone = 0
            # for team in teamNumbers:
            #     # if not os.path.exists(f"teamInfo/{team}.json") or getLastUpdatedYear(team) < datetime.now():
            #     pullTeamData(team)
            #     teamsDone += 1
            #     # #send_notifcation(f"Data has been collected for {teamsDone}/{len(teamNumbers)} teams from {eventCode}")
            #     clear()
            #     # #send_notifcation(f"Data collection complete for {len(teamNumbers)} teams from {eventCode}")
            #     print(f"Data collection complete for {teamsDone}/{len(teamNumbers)} teams from {eventCode}")
            # currentYear = datetime.now().year
        elif choice == 13:
            clear()
            print("Exiting...")
            clear()
            break
        # elif choice == 14:
            
            # with open("events.json", "w") as file:
            #     json.dump(getEvents(), file, indent=4)
    input("Press Enter to continue...")