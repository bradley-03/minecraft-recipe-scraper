import os
import zipfile
import shutil

def extract_jar (verName):
    try:
        if os.path.exists('./jars/data'):
            print("Deleting existing recipes")
            shutil.rmtree('./jars/data')

        with zipfile.ZipFile(f'./jars/{verName}.jar', 'r') as zip_ref:
            for member in zip_ref.namelist():
                if member.startswith("data/minecraft/recipe/"):
                    zip_ref.extract(member, './jars')

        print("Finished extracting! Cleaning up jar directory.")
        os.remove(f'./jars/{verName}.jar')
    except Exception as e:
        print(e)
        print("Something went wrong while extracting jar file.")