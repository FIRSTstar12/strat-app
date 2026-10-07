# strat-app Function Reference

## main.py

No functions defined here — this is the menu loop that ties everything together and calls functions from the other files.

## teamFunctions.py

**`has_happened(event)`**
Checks whether an event has already started, so future events are skipped.
Used in: `addEventStats`

**`eventStats(teamNumber, eventKey)`**
Gets a team's rank and average ranking points for one event.
Used in: `addEventStats`

**`getOPR(teamNumber, eventKey)`**
Gets a team's OPR (a score-contribution rating) for one event.
Used in: `addEventStats`

**`getInfo(data)`**
Prints a team's name, city, and rookie year.
Used in: nowhere currently — not called anywhere in the project.

**`getTeamMatches(team, year)`**
Fetches all of a team's matches for a given year.
Used in: `calculateStats`

**`addEventStats(stats, teamNumber, year)`**
Adds event-level numbers (rank, ranking points, OPR, events attended) into a stats dictionary. Only counts events that have already started.
Used in: `calculateStats`

**`calculateStats(teamNumber, year)`**
The main stats engine — builds a full stats dictionary for one team/year (wins, losses, scores, streaks, etc).
Used in: `main.py` (option 1, when the team isn't saved yet), `getLifetimeStats`, `utilityFunctions.py` (`pullTeamData`)

**`printStats(stats)`**
Prints a stats dictionary in a readable format.
Used in: `main.py` (options 1, 2, and 10)

**`getTeam(teamNumber)`**
Fetches a team's basic profile info (name, city, rookie year, etc).
Used in: `main.py` (option 1), `calculateStats`, `getLifetimeStats`, `utilityFunctions.py` (`pullTeamData`)

**`compareTeams(team1, team2, year)`**
Builds and prints a side-by-side comparison table for two teams, including their rating.
Used in: `main.py` (option 3)

**`getTeamScore(match, teamNumber)`**
Pulls out a team's score and the opposing score from a single match.
Used in: `calculateStats`

**`getLifetimeStats(teamNumber)`**
Loops through every year since a team's rookie year and calculates stats for each.
Used in: `utilityFunctions.py` (`pullTeamData`) — not used in `main.py`'s option 2, which reads saved data instead.

**`pullMultipleTeamData(teamNumbers)`**
Pulls data for a list of teams, skipping any that were already updated this year.
Used in: `main.py` (option 9, manual entry)

## predictionFunctions.py

**`get_percentiles(all_stats, key)`**
Works out how each team places against the others for one stat, with ties shared evenly.
Used in: `rank_teams`

**`rank_teams(all_stats)`**
Ranks a group of teams using percentile scores across several stats.
Used in: nowhere currently — not called anywhere in the project.

**`compute_min_max(stats_list)`**
Finds the lowest and highest value of each rating stat across a group of teams.
Used in: `calculateRating` callers — `predictTeams`, `findBestAlliance`, `findYourBestAlliance`, `getTopThreeAlliances`, `compareAlliances`, `compareTeams`

**`normalize(value, min_value, max_value)`**
Turns a stat into a 0-to-1 score based on where it falls between the lowest and highest in the group.
Used in: `calculateRating`

**`calculateRating(stats, mins, maxs)`**
Turns a stats dictionary into one overall rating number using a weighted formula. Needs the group's lowest/highest values so each team is judged against the others being compared.
Used in: `predictTeams`, `findBestAlliance`, `findYourBestAlliance`, `getTopThreeAlliances`, `allianceFunctions.py` (`compareAlliances`), `teamFunctions.py` (`compareTeams`)

**`predictTeams(team1, team2, year)`**
Compares two teams' ratings and returns the predicted winner (or a tie).
Used in: `main.py` (option 4)

**`findBestAlliance(teams, year)`**
Tries every three-team combination and returns the single highest-rated alliance.
Used in: nowhere currently — imported in `main.py` but its call is commented out.

**`findYourBestAlliance(yourTeam, teams, year)`**
Same as above, but your team is always one of the three.
Used in: nowhere currently — meant for menu option 12 once it is built.

**`getTopThreeAlliances(teams, year)`**
Finds the three best alliances that don't share any teams.
Used in: `main.py` (option 10)

## allianceFunctions.py

**`buildAlliance()`**
Prompts the user for three team numbers and returns them as a list.
Used in: `main.py` (option 5)

**`compareAlliances(alliance1, alliance2, year, internet)`**
Adds up the ratings of two 3-team alliances and prints which one is predicted to win.
Used in: `main.py` (option 5)

**`getAllianceDetails(alliance, year, internet)`**
Loads the saved season stats for each team in an alliance.
Used in: `main.py` (option 10)

## eventFunctions.py

**`getMatchInfo(match_key)`**
Fetches raw data for one specific match.
Used in: `main.py` (option 6)

**`getEventInfo(event)`**
Fetches all matches for an event and prints each match's level and number.
Used in: `main.py` (option 7)

**`getTeamEvents(teamNumber, year)`**
Gets the list of events a team attended in a given year.
Used in: `addEventStats` (in `teamFunctions.py`)

**`getEventTeams(event)`**
Gets the list of team numbers that attended a given event.
Used in: `main.py` (options 9 and 10, when using an event code)

## readingData.py

**`getEvents()`**
Fetches the list of events from TBA and returns each one's key, name, code, type, and year.
Used in: nowhere currently — imported in `main.py`, but its call is commented out.

## Team.py

**`Team` (class)**
A simple placeholder holding a team number plus empty slots for auto, teleop, endgame, and defense data.
Used in: nowhere currently — set aside for future scouting features.

## utilityFunctions.py

**`get_team_numbers(folder)`**
Lists team numbers already saved in a folder, based on filenames.
Used in: `teamFunctions.py` (`pullMultipleTeamData`)

**`getLastUpdatedYear(teamnumber)`**
Checks when a saved team file was last modified.
Used in: `teamFunctions.py` (`pullMultipleTeamData`)

**`send_notification(message)`**
Sends a Discord webhook message.
Used in: nowhere currently — every call is commented out. The file still needs `WEBHOOK_URL` in `keys.py` to start.

**`clear()`**
Clears the terminal screen.
Used in: everywhere — `main.py`, `teamFunctions.py`, `allianceFunctions.py`, `intro`, `options`

**`wait(sec)`**
Pauses execution for a number of seconds.
Used in: `intro`

**`pullTeamData(teamNumber)`**
Fetches a team's profile and saves it to a JSON file. If the team was never saved, it pulls their full history; if it was, it only refreshes the current year.
Used in: `main.py` (options 2, 3, 4, 8, 9, 10), `allianceFunctions.py`, `pullMultipleTeamData`

**`intro()`**
Prints the welcome message when the program starts.
Used in: `main.py`

**`options()`**
Displays the menu (options 1–13) and gets a valid choice from the user.
Used in: `main.py`

---

**Notes:**

Never called anywhere (dead code you could either wire in or remove): `getInfo`, `rank_teams`, `findBestAlliance`, `getEvents`, `send_notification`, and the `Team` class. `findYourBestAlliance` is waiting for menu option 12.