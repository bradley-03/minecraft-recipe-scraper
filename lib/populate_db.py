import os.path
import json
from lib.db import recipesCollection
import shutil

recipespath = './jars/data/minecraft/recipe'

def populate_db ():
    try:
        print("Repopulating DB with recipes.")
        recipesCollection.drop()

        for item in os.listdir(recipespath):
             with open(f'{recipespath}/{item}', 'r') as file:
                recipe = json.load(file)
                recipesCollection.insert_one(recipe)

        print("Finished populating recipes! Cleaning up jar directory.")
        shutil.rmtree('./jars/data')
    except Exception as e:
        print(e)
        print("Something went wrong populating db with recipes.")
    