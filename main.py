import requests
from datetime import datetime
import time
from lib.downloadjar import download_from_version
from lib.extractjar import extract_jar
from lib.populate_db import populate_db
from lib.db import dataCollection

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
        if found and latestVer and latestVer["id"] != found["ver"]:
            print("THERE'S A NEW VERSION!")
            update_recipes(latestVer)
            return dataCollection.update_one({"type": "latest_ver"}, {"$set" : {"ver": latestVer["id"], "updateTime": datetime.now()}})
        elif not found and latestVer:
            print("VERSION NOT FOUND, ASSUMING THIS IS FIRST EXECUTION, DB WILL BE REFRESHED")
            update_recipes(latestVer)
            dataCollection.insert_one({"type": "latest_ver", "ver": latestVer["id"]})
        else:
            print("No new update found.")
    except Exception as e:
        print(e)
        print("Something went wrong fetching latest version.")

while True:
    ver_check()
    # sleep for desired time
    time.sleep(UPDATE_CHECK_DELAY)