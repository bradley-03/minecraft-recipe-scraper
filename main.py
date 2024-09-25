import requests
from datetime import datetime
import time
from lib.downloadjar import download_from_version
from lib.extractjar import extract_jar
from lib.populate_db import populate_db
from lib.db import dataCollection
from lib.db import recipesCollection
from config import config

VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

def update_recipes (verData):
    # download jar
    download_from_version(verData["url"])
    # extract recipes from jar
    extract_jar(verData["id"]) 
    # populate db with recipes
    populate_db()
    print("Finished populating DB!")

def ver_check ():
    try:
        res = requests.get(VERSION_MANIFEST_URL)
        resData = res.json()
        
        latestReleaseName = resData["latest"]["release"]
        latestVer = resData["versions"][0]
        
        if config["ALLOW_SNAPSHOTS"] == False:
            for ver in resData["versions"]: # find latest version that isn't a snapshot
                if ver["id"] == latestReleaseName:
                    latestVer = ver
                    break

        found = dataCollection.find_one({"data_type": "latest_ver"})

        if not found:
            print("LATEST VERSION NOT FOUND, ASSUMING THIS IS FIRST EXECUTION, DB WILL BE REFRESHED")
            update_recipes(latestVer)
            dataCollection.insert_one({
                "data_type": "latest_ver", 
                "ver": latestVer["id"], 
                "ver_type": latestVer["type"]
            })
            found = dataCollection.find_one({"data_type": "latest_ver"})
        
        if found["ver"] != latestVer["id"]:
            print("New version found!")
            update_recipes(latestVer)
            return dataCollection.update_one({"data_type": "latest_ver"}, {"$set" : {"ver": latestVer["id"], "ver_type": latestVer["type"], "updateTime": datetime.now()}})
        else:
            print("No new version found")

        recipe_count = recipesCollection.count_documents({})
        if recipe_count < config["POPULATE_ERROR_THRESHOLD"] and found:
            print(f"Version found and recipe count is lower than {config["POPULATE_ERROR_THRESHOLD"]}, assuming something went wrong when populating and retrying.")
            update_recipes(latestVer)

    except Exception as e:
        print(e)
        print("Something went wrong fetching latest version.")

while True:
    ver_check()
    # sleep for desired time
    time.sleep(config["UPDATE_CHECK_DELAY"])