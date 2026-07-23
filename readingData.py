import pandas as pd
from keys import SCOUTING_DATA_PATH

stats = pd.read_csv(SCOUTING_DATA_PATH)
stats = stats.dropna(subset=["Team"])
data = []

for index, team in stats.iterrows():

    total = (
        team["Average Auto Total Shots"] +
        team["Average Teleop Total Shots"]
    )

    data.append(f"Team {team['Team']} took {total:.2f} shots")
