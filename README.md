# strat-app

A small command-line tool to help FIRST Robotics Competition (FRC) teams analyze team and event
statistics using The Blue Alliance (TBA) API. Use it to fetch team info, compute season/lifetime
stats, compare teams or alliances, predict winners, find the best alliances at an event, and save
team data locally.

## Requirements

- Python 3.8+
- Packages listed in `requirements.txt` (`requests`, `keyboard`, `pandas`)

Install them with:

```powershell
pip install -r requirements.txt
```

> Note: on Linux, the `keyboard` package needs the program to be run with admin (sudo) rights
> because it listens for the `q` key.

## Setup

1. Get a TBA API key from The Blue Alliance (https://www.thebluealliance.com/).

2. Create a file called `keys.py` in the project folder with the following code, replacing the
   placeholder values:

```python
API_KEY = "YOUR API KEY HERE"
BASE_URL = "https://www.thebluealliance.com/api/v3"

# Used by utilityFunctions.py. Notifications are currently turned off in the code,
# but the program still looks for this value when it starts, so keep it here.
# Any text is fine if you aren't using Discord notifications.
# WEBHOOK_URL = "YOUR DISCORD WEBHOOK URL HERE"

headers = {
    "X-TBA-Auth-Key": API_KEY,
    "accept": "application/json"
}
```

3. The `teamInfo` folder is where all saved team `.json` files go. If it is missing, the program
   will offer to create it for you when it starts. You can also create it yourself.

4. Connect to the internet the first time so you can pull data.

## Running

Start the CLI:

```powershell
python main.py
```

When the program starts it asks two questions:

- **Do you have an internet connection?** If you answer `n`, you can still use any team data you
  have already saved, but you cannot pull anything new.
- **Would you like to repull all team data?** If you answer `y`, option 10 (when using an event
  code) refreshes every team's data before ranking alliances.

Then follow the on-screen menu. The program will prompt for team numbers, years, event/match
codes, and other inputs depending on your choice. Press `q` at the menu to quit quickly.

## Menu options (quick reference)

- `1` Look up stats for one team for one season (enter team number and year).
- `2` Look up stats for one team for every season they participated in (lifetime stats).
- `3` Compare two teams for a given year.
- `4` Predict who would win between two teams based on weighted statistical rating.
- `5` Predict which alliance (three teams each) would win, using the current year.
- `6` Get match data by match code.
- `7` Get event data by event code.
- `8` Pull new team data for one team from The Blue Alliance API and save to `teamInfo/`.
- `9` Pull new team data for multiple teams and save to `teamInfo/`. Enter team numbers by hand
  (comma-separated) or enter an event code to pull every team at that event.
- `10` Find the best alliances for a set of teams. Enter team numbers by hand or enter an event
  code. Shows the top three alliances (with no team used twice) and each team's stats.
- `11` Read the CSV file (early/experimental, not fully working yet).
- `12` Build an alliance around one team (not available yet, planned for the future).
- `13` Exit.

## How ratings work

Each team gets a rating from 0 to 1 based on win percentage, average score, longest win streak,
average ranking points, average OPR, events attended, and average rank. Each stat is scored
against the other teams being compared, so a team's rating depends on who it is being compared
with. An alliance's rating is the sum of its three teams' ratings.

## Data and outputs

- Saved team data is written to the `teamInfo/` folder as `<teamNumber>.json`. Those files
  include team info and a `stats` object with per-year statistics computed from match and event
  data.
- The first time a team is pulled, its full history (rookie year to now) is saved. After that,
  pulling again only refreshes the current year, which is much faster.

## Key files

- `main.py` — CLI menu and main control flow
- `teamFunctions.py` — fetching team/match data, computing stats, comparing teams
- `predictionFunctions.py` — rating calculation, match prediction, best-alliance search
- `allianceFunctions.py` — build/compare alliances
- `eventFunctions.py` — match/event API helpers
- `readingData.py` — pulls the list of events from TBA (not used by the menu yet)
- `utilityFunctions.py` — console helpers, pull/save logic, and the menu
- `Team.py` — placeholder team class for future scouting data (not used yet)
- `keys.py` — your API key, base URL, and webhook (you create this file; see Setup)
- `referanceGuide.md` — a plain-English guide to every function

## Notes & troubleshooting

- The program depends on the TBA API and your API key. If requests fail, check the key and look
  for rate limits or internet problems.
- If the program crashes right at startup with a message about `WEBHOOK_URL`, add that line to
  `keys.py` (see Setup).
- If you see a "file not found" error for a team, pull that team's data first (option 8 or 9).
- If it errors please make a pr so I can fix it

---