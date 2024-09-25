from pymongo import MongoClient
from config import config

client = MongoClient(config["MONGODB_URL"])

db = client[config["MONGODB_DB_NAME"]]

dataCollection = db["data"]
recipesCollection = db["recipes"]