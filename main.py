from models.connection import get_connection
from config import teams


def get_winners_count(year):
    final_dict = {}
    mycol = get_connection()
    winners_dict = {}
    for team in teams:
        query = {"$and":[{"season":year},{"winner":team}]}
        count = mycol.find(query).count()
        winners_dict[team] = count
    top_winners = sorted(winners_dict.items(), key=lambda x:x[1], reverse=True)[:4]
    for winner in top_winners:
        final_dict[winner[0]] = winner[1]
    winner = top_winners[0]
    return final_dict, winner


def get_max_toss_winner(year):
    final_dict = {}
    mycol = get_connection()
    winners_dict = {}
    for team in teams:
        query = {"$and":[{"season":year},{"winner":team}]}
        count = mycol.find(query).count()
        winners_dict[team] = count
    top_toss_winner = sorted(winners_dict.items(), key=lambda x:x[1], reverse=True)[0]
    print("******top", top_toss_winner)
    final_dict[top_toss_winner[0]] = top_toss_winner[1]
    return final_dict


def get_max_player_of_the_match(year):
     final_dict = {}
     mycol = get_connection()
     player_of_match_list = mycol.distinct("player_of_match", {"season":year})
     max_pom = {}
     for player in player_of_match_list:
         query = {"$and":[{"player_of_match":player},{"season":year}]}
         count = mycol.find(query).count()
         max_pom[player] = count
     max_pom_winner = sorted(max_pom.items(), key=lambda x:x[1], reverse=True)[0]
     final_dict[max_pom_winner[0]] = max_pom_winner[1]
     return final_dict


def max_hosted_location(year):
    final_dict = {}
    mycol = get_connection()
    max_location = mycol.distinct("venue", {"season":year})
    max_host = {}
    for loc in max_location:
        query = {"$and":[{"season":"2017"}, {"venue":"Rajiv Gandhi International Stadium, Uppal"}]}
        count = mycol.find(query).count()
        max_host[loc] = count
    max_host_loc = sorted(max_host.items(), key=lambda x:x[1], reverse=True)[0]
    print("max_host_loc", max_host_loc)
    final_dict[max_host_loc[0]] = max_host_loc[1]
    return final_dict


def max_number_of_wins_per_location(year, won_team):
    mycol = get_connection()
    max_location = {}
    distinct_won_locations = mycol.distinct("venue", {"$and":[{"season":year},{"winner":won_team[0]}]})
    for loc in distinct_won_locations:
        query = {"$and":[{"season":year},{"winner":won_team[0]},{"venue":loc}]}
        count = mycol.find(query).count()
        max_location[loc] = count
    max_location_name = sorted(max_location.items(), key=lambda x:x[1], reverse=True)[0]
    max_location_name_ = {}
    max_location_name_[max_location_name[0]] = max_location_name[1]
    max_location_name_["team"] = won_team[0]
    return max_location_name_


def per_of_teams_to_bat(year):
    mycol = get_connection()
    total_no_matches = 60
    query = {"$and":[{"toss_decision":"bat"},{"season":year}]}
    bat_choosed =  mycol.find(query).count()
    percentage = (bat_choosed/total_no_matches)*100
    return percentage

def team_higest_run(year):
     mycol = get_connection()
     final_dict = {}
     query = {"season":year}
     record = mycol.find(query).sort([("win_by_runs",-1)]).limit(1)
     for rec in record:
         final_dict["team"] = rec.get("winner")
         final_dict["win_by_runs"] = rec.get("win_by_runs")
     return final_dict

def team_highest_wicket(year):
    mycol = get_connection()
    final_dict = {}
    query = {"season":year}
    record = mycol.find(query).sort([("win_by_wickets",-1)]).limit(1)
    for rec in record:
        final_dict["team"] = rec.get("winner")
        final_dict["win_by_runs"] = rec.get("win_by_wickets")
    return final_dict


def team_and_toss_won(year):
    mycol = get_connection()
    sum_ = 0
    for team in teams:
        query = {"$and":[{"season":year},{"winner":team},{"toss_winner":team}]}
        count = mycol.find(query).count()
        sum_ = sum_ +count
    return sum_

