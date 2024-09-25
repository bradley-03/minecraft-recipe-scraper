from pymongo import MongoClient
import requests
from datetime import datetime
import time

VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
UPDATE_CHECK_DELAY = 5

client = MongoClient("mongodb://localhost:27017")
db = client["mc-recipe-scrape"]

dataCollection = db["data"]

def getLatestVersion ():
    try:
        res = requests.get(VERSION_MANIFEST_URL)
        resData = res.json()

        found = dataCollection.find_one({"type": "latest_ver"})
        if found and resData["versions"][0]["id"] != found["ver"]:
            return dataCollection.update_one({"type": "latest_ver"}, {"$set" : {"ver": resData["versions"][0]["id"], "updateTime": datetime.now()}})
        elif not found:
            dataCollection.insert_one({"type": "latest_ver", "ver": resData["versions"][0]["id"]})
        else:
            print("Already has latest version.")
    except Exception as e:
        print(e)
        print("Something went wrong fetching latest version.")


while True:
    getLatestVersion()
    # sleep for desired time
    time.sleep(UPDATE_CHECK_DELAY)