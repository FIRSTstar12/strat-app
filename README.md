# strat-app

A small command-line tool to help FIRST Robotics Competition (FRC) teams analyze team and event
statistics using The Blue Alliance (TBA) API. Use it to fetch team info, compute season/lifetime
stats, compare teams or alliances, predict winners, and save team data locally.

## Requirements

- Python 3.8+
- See `requirements.txt` (notably `requests` and `keyboard`)

## Setup

1. Obtain a TBA API key from The Blue Alliance (https://www.thebluealliance.com/) and set it in
	`keys.py` by replacing the `API_KEY` value. The program uses `keys.py` to build API requests.

2. Ensure you are connected to the internet when running the program.

## Running

Start the CLI:

```powershell
python main.py
```

Follow the on-screen menu. The program will prompt for team numbers, years, event/match codes,
and other inputs depending on your choice.

## Menu options (quick reference)

- `1` Look up stats for one team for one season (enter team number and year).
- `2` Look up stats for one team for every season they participated in (lifetime stats).
- `3` Compare two teams for a given year.
- `4` Predict who would win between two teams based on weighted statistical rating.
- `5` Predict which alliance (three teams each) would win.
- `6` Get match data by match code.
- `7` Get event data by event code.
- `8` Pull new team data for one team from The Blue Alliance API and save to `teamInfo/`.
- `9` Pull new team data for multiple teams (comma-separated list) and save to `teamInfo/`.
- `10` Exit.

## Data and outputs

- Saved team data is written to the `teamInfo/` folder as `<teamNumber>.json` when you use the
	pull-data options. Those files include team metadata and a `stats` object containing per-year
	statistics computed from match and event data.

## Key files

- `main.py` — CLI menu and main control flow
- `teamFunctions.py` — fetching team/match data, computing stats
- `predictionFunctions.py` — rating calculation and match prediction
- `allianceFunctions.py` — build/compare alliances
- `eventFunctions.py` — match/event API helpers
- `utilityFunctions.py` — console helpers and pull/save logic
- `keys.py` — API key and base URL (replace `API_KEY` with your own)

## Notes & troubleshooting

- The program depends on the TBA API and your API key; if requests fail, verify the key and
	check for rate limits or network issues.
- The `keyboard` package is used for a quit check; on some systems it may require elevated
	permissions. If you run into issues, you can modify `main.py` to remove/replace that check.

## Contributing

Feel free to open issues or submit PRs to improve error handling, refactor input handling,
or add unit tests.

---
