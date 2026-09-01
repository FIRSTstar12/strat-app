import pandas as pd
import requests
from wpiutil import json
from keys import SCOUTING_DATA_PATH
import keys

stats = pd.read_csv(SCOUTING_DATA_PATH)
stats = stats.dropna(subset=["Team"])
data = []

for index, team in stats.iterrows():

    total = (
        team["Average Auto Total Shots"] +
        team["Average Teleop Total Shots"]
    )

    data.append(f"Team {team['Team']} took {total:.2f} shots")
def getEvents():
    
    events = requests.get(keys.BASE_URL + "/events", headers=keys.headers).json()

    event_list = []

    for event in events:
        event_list.append({
            "key": event["key"],
            "name": event["name"],
            "event_code": event["event_code"],
            "event_type": event["event_type"],
            "year": event["year"]
        })

        
    return event_list