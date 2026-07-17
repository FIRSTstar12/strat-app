# strat-app Function Reference

## main.py

No functions defined here — this is the menu loop that ties everything together and calls functions from the other files.

## teamFunctions.py

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
Adds event-level numbers (rank, ranking points, OPR, events attended) into a stats dictionary.
Used in: `calculateStats`

**`calculateStats(teamNumber, year)`**
The main stats engine — builds a full stats dictionary for one team/year (wins, losses, scores, streaks, etc).
Used in: `main.py` (options 1, 2, 3, 4), `compareTeams`, `allianceFunctions.py`, `predictionFunctions.py`, `getLifetimeStats`

**`printStats(stats)`**
Prints a stats dictionary in a readable format.
Used in: `main.py` (options 1 and 2)

**`getTeam(teamNumber)`**
Fetches a team's basic profile info (name, city, rookie year, etc).
Used in: `main.py`, `compareTeams`, `allianceFunctions.py`, `getLifetimeStats`, `utilityFunctions.py`

**`compareTeams(team1, team2, year)`**
Builds and prints a side-by-side comparison table for two teams.
Used in: `main.py` (option 3)

**`getTeamScore(match, teamNumber)`**
Pulls out a team's score and the opposing score from a single match.
Used in: `calculateStats`

**`getLifetimeStats(teamNumber)`**
Loops through every year since a team's rookie year and calculates stats for each.
Used in: `utilityFunctions.py` (`pullTeamData`) — not used in `main.py`'s option 2, which repeats this logic manually instead.

## predictionFunctions.py

**`calculateRating(stats)`**
Turns a stats dictionary into one overall rating number using a weighted formula.
Used in: `predictTeams`, `allianceFunctions.py` (`compareAlliances`)

**`predictTeams(team1, team2, year)`**
Compares two teams' ratings and returns the predicted winner (or a tie).
Used in: `main.py` (option 4)

## allianceFunctions.py

**`buildAlliance()`**
Prompts the user for three team numbers and returns them as a list.
Used in: `main.py` (option 5)

**`compareAlliances(alliance1, alliance2, year)`**
Adds up the ratings of two 3-team alliances and prints which one is predicted to win.
Used in: `main.py` (option 5)

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
Used in: nowhere currently — not called anywhere in the project.

## utilityFunctions.py

**`get_team_numbers(folder)`**
Lists team numbers already saved in a folder, based on filenames.
Used in: `main.py` (option 9)

**`getLastUpdatedYear(teamnumber)`**
Checks when a saved team file was last modified, by year.
Used in: `main.py` (option 9)

**`send_notification(message)`**
Sends a Discord webhook message, plus a desktop popup notification.
Used in: `main.py` (multiple options), `compareTeams`, `allianceFunctions.py`, `pullTeamData`

**`clear()`**
Clears the terminal screen.
Used in: everywhere — `main.py`, `teamFunctions.py`, `allianceFunctions.py`, `intro`, `options`

**`wait(sec)`**
Pauses execution for a number of seconds.
Used in: `intro`

**`pullTeamData(teamNumber)`**
Fetches a team's profile and lifetime stats, then saves it all to a JSON file.
Used in: `main.py` (options 8 and 9)

**`intro()`**
Prints the welcome message when the program starts.
Used in: `main.py`

**`options()`**
Displays the menu and gets a valid choice from the user.
Used in: `main.py`

---

**Notes:**

`getInfo` and `getEventTeams` are fully written but never called anywhere — dead code you could either wire in or remove.