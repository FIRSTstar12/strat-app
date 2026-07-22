"""
import teamFunctions
import json
import statistics


def get_percentiles(all_stats, key):
    
    
    values = [player[key] for player in all_stats]
    n = len(values)

    percentiles = {}
    for player in all_stats:
        value = player[key]
        beaten = sum(1 for v in values if v < value)
        tied = sum(1 for v in values if v == value)

        percentile = (beaten + 0.5 * (tied - 1)) / (n - 1) if n > 1 else 0.5
        percentiles[id(player)] = percentile

    return percentiles


def rank_teams(all_stats):
    
    keys_and_weights = {
        "win_percentage": 0.25,
        "average_score": 0.20,
        "longest_win_streak": 0.05,
        "average_rp": 0.15,
        "average_opr": 0.15,
        "events_attended": 0.10,
    }

    # Calculate percentiles once per stat
    all_percentiles = {}
    for key in keys_and_weights:
        all_percentiles[key] = get_percentiles(all_stats, key)

    # average_rank is reversed — lower rank is better
    rank_percentiles = get_percentiles(all_stats, "average_rank")

    # Score every team using the precomputed percentiles
    scored_teams = []
    for team in all_stats:
        score = 0
        for key, weight in keys_and_weights.items():
            score += all_percentiles[key][id(team)] * weight

        score += (1 - rank_percentiles[id(team)]) * 0.10
        scored_teams.append((team, score))

    scored_teams.sort(key=lambda x: x[1], reverse=True)
    return scored_teams
'''
    ranked = rank_teams(all_stats)

    for team, score in ranked:
        print(team["name"], round(score, 3))
'''
def normalize(value, min_value, max_value):
    if max_value == min_value:
        return 0  # avoid divide-by-zero if everyone has the same value
    return (value - min_value) / (max_value - min_value)

def calculateRating(stats, mins, maxs):
    return (
        normalize(stats["win_percentage"], mins["win_percentage"], maxs["win_percentage"]) * 0.25 +
        normalize(stats["average_score"], mins["average_score"], maxs["average_score"]) * 0.20 +
        normalize(stats["longest_win_streak"], mins["longest_win_streak"], maxs["longest_win_streak"]) * 0.05 +
        normalize(stats["average_rp"], mins["average_rp"], maxs["average_rp"]) * 0.15 +
        normalize(stats["average_opr"], mins["average_opr"], maxs["average_opr"]) * 0.15 +
        normalize(stats["events_attended"], mins["events_attended"], maxs["events_attended"]) * 0.10 +
        normalize(1 / (stats["average_rank"] + 1), 
                  1 / (maxs["average_rank"] + 1), 
                  1 / (mins["average_rank"] + 1)) * 0.10
    )

def predictTeams(team1, team2, year):
    with open(f"teamInfo/{team1}.json", 'r') as file:
        data = json.load(file)
    team1Stats = data['stats'][str(year)]
    with open(f"teamInfo/{team2}.json", 'r') as file:
        info = json.load(file)
    team2Stats = info['stats'][str(year)]

    team1Rating = calculateRating(team1Stats)
    team2Rating = calculateRating(team2Stats)

    print(f"\n{team1} Rating: {team1Rating:.2f}")
    print(f"{team2} Rating: {team2Rating:.2f}")

    if team1Rating > team2Rating:
        return team1
    elif team2Rating > team1Rating:
        return team2
    else:
        return None

def findBestAlliance(teams, year):
    bestAlliance = None
    bestRating = 0

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            for k in range(j + 1, len(teams)):
                alliance = [teams[i], teams[j], teams[k]]
                rating = 0
                for team in alliance:
                    with open(f"teamInfo/{team}.json", 'r') as file:
                        data = json.load(file)
                    teamStats = data['stats'][str(year)]
                    rating += calculateRating(teamStats)

                if rating > bestRating:
                    bestRating = rating
                    bestAlliance = alliance
                    print(f"Current Best Alliance: {bestAlliance}, Rating: {bestRating:.2f}\n")
                
                print(f"Alliance: {alliance}, Rating: {rating:.2f}\n")
                

    return bestAlliance, bestRating
"""

import teamFunctions
import json

def calculateRating(stats):
    return (
        stats["win_percentage"] * 0.25 +
        stats["average_score"] * 0.20 +
        stats["longest_win_streak"] * 0.05 +
        stats["average_rp"] * 0.15 +
        stats["average_opr"] * 0.15
    )

def predictTeams(team1, team2, year):
    with open(f"teamInfo/{team1}.json", 'r') as file:
        data = json.load(file)
    team1Stats = data['stats'][str(year)]
    with open(f"teamInfo/{team2}.json", 'r') as file:
        info = json.load(file)
    team2Stats = info['stats'][str(year)]

    team1Rating = calculateRating(team1Stats)
    team2Rating = calculateRating(team2Stats)

    print(f"\n{team1} Rating: {team1Rating:.2f}")
    print(f"{team2} Rating: {team2Rating:.2f}")

    if team1Rating > team2Rating:
        return team1
    elif team2Rating > team1Rating:
        return team2
    else:
        return None

def findBestAlliance(teams, year):
    bestAlliance = None
    bestRating = 0

    for i in range(len(teams)):
        for j in range(i + 1, len(teams)):
            for k in range(j + 1, len(teams)):
                alliance = [teams[i], teams[j], teams[k]]
                rating = 0
                for team in alliance:
                    with open(f"teamInfo/{team}.json", 'r') as file:
                        data = json.load(file)
                    teamStats = data['stats'][str(year)]
                    rating += calculateRating(teamStats)

                if rating > bestRating:
                    bestRating = rating
                    bestAlliance = alliance
                    print(f"Current Best Alliance: {bestAlliance}, Rating: {bestRating:.2f}\n")
                
                print(f"Alliance: {alliance}, Rating: {rating:.2f}\n")
                

    return bestAlliance, bestRating