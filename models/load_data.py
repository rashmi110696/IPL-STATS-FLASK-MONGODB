import csv

from models.connection import get_connection

def load_data():
    mycol = get_connection()
    _dict = {}
    csvfile = "matches.csv"
    with open(csvfile) as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for rows in csv_reader:
            _id = rows["id"]
            _dict[_id] = rows
            x = mycol.insert_one(_dict[_id])
