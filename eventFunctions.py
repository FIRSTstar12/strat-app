import requests
import keys


def getMatchInfo(match_key):
    url = f"https://www.thebluealliance.com/api/v3/match/{match_key}"

    match_info = requests.get(
        url,
        headers=keys.headers
    ).json()

    return match_info

def getEventInfo(event):
    url = f"https://www.thebluealliance.com/api/v3/event/{event}/matches"

    matches = requests.get(
        url,
        headers=keys.headers
    ).json()

    for match in matches:
        print(match["comp_level"], match["match_number"])

def getTeamEvents(teamNumber, year):
    url = f"{keys.BASE_URL}/team/frc{teamNumber}/events/{year}"

    events = requests.get(
        url,
        headers=keys.headers
    ).json()

    return events

def getEventTeams(event):
    url = f"{keys.BASE_URL}/event/{event}/teams"

    response = requests.get(
        url,
        headers=keys.headers
    )

    if not response.ok:
        print(f"Error {response.status_code}: {response.text}")
        return []

    teams = response.json()

    if teams is None:
        print(f"No team data found for event {event}.")
        return []

    return [team["team_number"] for team in teams]