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