import os
import time
import json
from datetime import datetime
from teamFunctions import getLifetimeStats

from teamFunctions import getTeam

currentYear = datetime.now().year

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait(sec):
    time.sleep(sec)

def pullTeamData(teamNumber):
    data = getTeam(teamNumber)
    lifetimeStats = getLifetimeStats(teamNumber)
    folder = "teamInfo"
    filename = f"{teamNumber}.json"
    filepath = os.path.join(folder, filename)

    if data is None:
        print(f"No data returned for team {teamNumber}, skipping save.")
        return

    if os.path.exists(filepath):
        print("File found, overwriting...")
    else:
        print("File not found, creating new one...")

    data["stats"] = lifetimeStats

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)

def intro():
    clear()
    print("Welcome to the strat helper!")
    wait(1.5)
    print("Note you do need to be connected to the internet to use the program")
    wait(2)
    input("Press Enter to continue")
    clear()

def options():
    clear()
    print("Options:")
    print("1. Look up stats for one team for one season")
    print("2. Look up the stats for one team for every season they have ever particpated in")
    print("3. Compare two teams")
    print("4. Predict who will win between two teams")
    print("5. Predict which alliance will win")
    print("6. Get match data")
    print("7. Get event data")
    print("8. Pull new team data for one team from The Blue Alliance API")
    print("9. Pull new team data for multiple teams from The Blue Alliance API")
    print("10. Exit")

    while True:
        choice = input("Please select an option (1-10): ")
        if choice.strip().isdigit():
            choice_int = int(choice)
            if 1 <= choice_int <= 10:
                return choice_int
        print("Invalid input. Please enter a number from 1 to 10.")
