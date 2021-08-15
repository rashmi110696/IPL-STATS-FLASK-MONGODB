import json
import pymongo, csv

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from loguru import logger

from config import teams
from models.connection import get_connection
from models.load_data import load_data
from main import get_winners_count, get_max_toss_winner, get_max_player_of_the_match, max_hosted_location, max_number_of_wins_per_location, per_of_teams_to_bat, team_higest_run, team_highest_wicket, team_and_toss_won

app = Flask(__name__)
api = Api(app)

args = reqparse.RequestParser()
args.add_argument("year", type=str, help="year is required", required=True)

connection = get_connection()

class IplStatsTopWinner(Resource):
    def get(self):
        final_dict = {"success":True, "result":{}}
        obtained_args = args.parse_args()
        year = obtained_args["year"]
        logger.debug("year obtained is {}".format(year))
        top_winners, winner = get_winners_count(year)
        top_toss_winner = get_max_toss_winner(year)
        max_player_of_match = get_max_player_of_the_match(year)
        max_hosted_location_name = max_hosted_location(year)
        max_number_of_wins_per_location_name = max_number_of_wins_per_location(year, winner)
        per_of_teams_to_bat_count = per_of_teams_to_bat(year)
        highest_margin_of_runs = team_higest_run(year)
        team_highest_wicket_ = team_highest_wicket(year)
        both_toss_and_won = team_and_toss_won(year)
        final_dict["result"]["top_4_winners"] = top_winners
        final_dict["result"]["top_toss_winner"] = top_toss_winner
        final_dict["result"]["top_player_of_match"] = max_player_of_match
        final_dict["result"]["top_max_matches_winner"] = winner
        final_dict["result"]["max_hosted_location"] = max_hosted_location_name
        final_dict["result"]["location_which_has_max_wins_for_top_team"] = max_number_of_wins_per_location_name
        final_dict["result"]["percentage_of_team_to_bat"] = str(round(per_of_teams_to_bat_count, 2))+"%"
        final_dict["result"]["highest_margin_of_runs"] = highest_margin_of_runs
        final_dict["result"]["highest_number_of_wickets"] = team_highest_wicket_
        final_dict["result"]["count_of_teams_won_both_toss_and_match"] = both_toss_and_won
        both_toss_and_won = team_and_toss_won(year)
        return jsonify(final_dict)

api.add_resource(IplStatsTopWinner, "/api/ipl_stats")

if __name__ == "__main__":
    load_data()
    app.run(debug=True)
