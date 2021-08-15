import pymongo
from loguru import logger

def get_connection():
    logger.info("Connecting to Mongodb")
    myclient = pymongo.MongoClient()
    mydb = myclient["ipl"]
    mycol = mydb["ipl_stats"]
    logger.info("Connected to Mongodb")
    return mycol

