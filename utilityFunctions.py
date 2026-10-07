import os
import time
import json
from datetime import datetime
import requests
from keys import WEBHOOK_URL
from teamFunctions import calculateStats, getLifetimeStats
from teamFunctions import getTeam
#from plyer import notification
from pathlib import Path

def get_team_numbers(folder):
    teams = []

    for file in Path(folder).iterdir():
        if file.is_file() and file.stem.isdigit():
            teams.append(int(file.stem))

    return sorted(teams)

def getLastUpdatedYear(teamnumber):
    file = Path(f"teamInfo/{teamnumber}.json")

    if not file.exists():
        return None
    last_updated_year = datetime.fromtimestamp(file.stat().st_mtime)

    return last_updated_year

# team_numbers = get_team_numbers("stats")

# print(team_numbers)

def send_notification(message):
    
    payload = {
        "content": message
    }

    # response = requests.post(WEBHOOK_URL, json=payload)

    # if response.status_code == 204:
    #     notification.notify(
    #     title="FRC Stats Analyzer",
    #     message="Discord notification sent!",
    #     timeout=5
    # )
    #     # print("Discord notification sent!")
    # else:
    #     print(f"Failed to send notification: {response.status_code}")
    #     notification.notify(
    #     title="FRC Stats Analyzer",
    #     message=f"Failed to send notification: {response.status_code}",
    #     timeout=5
    #     )
    #     # print(response.text)


currentYear = datetime.now().year

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait(sec):
    time.sleep(sec)

def pullTeamData(teamNumber):
    data = getTeam(teamNumber)
    # lifetimeStats = getLifetimeStats(teamNumber)
    folder = "teamInfo"
    filename = f"{teamNumber}.json"
    filepath = os.path.join(folder, filename)

    if os.path.exists(filepath):
        print(f"File found, refreshing this year's stats only for team {teamNumber}...")
        with open(filepath, 'r') as file:
            existing = json.load(file)

        stats = existing.get("stats", {})
        year = currentYear
        stats[str(year)] = calculateStats(teamNumber, year)
        data["stats"] = stats
    else:
        print(f"File not found, pulling full history for team {teamNumber}...")
        data["stats"] = getLifetimeStats(teamNumber)

    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)
    #send_notification(f"Data saved for team {teamNumber} {data['nickname']}")

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

    print("=" * 60)
    print("                    STRAT APP")
    print("=" * 60)
    print("                         OPTIONS")
    print("-" * 60)

    options_list = [
        "Look up stats for one team for one season",
        "Look up stats for one team across every season",
        "Compare two teams",
        "Predict who will win between two teams",
        "Predict which alliance will win",
        "Get match data",
        "Get event data",
        "Pull new team data for one team from The Blue Alliance API",
        "Pull new team data for multiple teams from The Blue Alliance API",
        "Find the best alliance for a set of teams",
        "Read the CSV file",
        "Build an alliance around one team",
        "Exit"
    ]

    for number, option in enumerate(options_list, start=1):
        print(f"  {number:>2}. {option}")

    print("-" * 60)

    while True:
        choice = input("\nSelect an option (1-13): ").strip()

        if choice.isdigit():
            choice_int = int(choice)

            if 1 <= choice_int <= 13:
                return choice_int

        print("Invalid input. Please enter a number from 1 to 13.")
