import pandas as pd
import requests
import json
#from wpiutil import json
#from keys import SCOUTING_DATA_PATH
import keys


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
