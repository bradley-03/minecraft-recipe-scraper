import requests
from datetime import datetime
import time
from lib.downloadjar import download_from_version
from lib.extractjar import extract_jar
from lib.populate_db import populate_db
from lib.db import dataCollection
from lib.db import recipesCollection

VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
UPDATE_CHECK_DELAY = 600

def update_recipes (verData):
    # download jar
    download_from_version(verData["url"])
    # extract recipes from jar
    extract_jar(verData["id"]) 
    # populate db with recipes
    populate_db()

def ver_check ():
    try:
        res = requests.get(VERSION_MANIFEST_URL)
        resData = res.json()

        found = dataCollection.find_one({"type": "latest_ver"})
        latestVer = resData["versions"][0]

        recipe_count = recipesCollection.count_documents({})

        if found and latestVer["id"] != found["ver"]:
            print("New version detected!")
            update_recipes(latestVer)
            return dataCollection.update_one({"type": "latest_ver"}, {"$set" : {"ver": latestVer["id"], "updateTime": datetime.now()}})
        elif not found:
            print("VERSION NOT FOUND, ASSUMING THIS IS FIRST EXECUTION, DB WILL BE REFRESHED")
            update_recipes(latestVer)
            dataCollection.insert_one({"type": "latest_ver", "ver": latestVer["id"]})
        elif found and recipe_count < 500:
            print("Version found and recipe count is lower than 500, assuming something went wrong when populating and retrying")
            update_recipes(latestVer)
        else:
            print("No new update found.")

    except Exception as e:
        print(e)
        print("Something went wrong fetching latest version.")

while True:
    ver_check()
    # sleep for desired time
    time.sleep(UPDATE_CHECK_DELAY)