from pymongo import MongoClient
from config import config

client = MongoClient(config["MONGODB_URL"])

db = client["mc-recipe-scrape"]

dataCollection = db["data"]
recipesCollection = db["recipes"]