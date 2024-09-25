from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["mc-recipe-scrape"]

dataCollection = db["data"]
recipesCollection = db["recipes"]