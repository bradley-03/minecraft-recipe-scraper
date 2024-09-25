import requests
import os.path
import os

def download_from_version (url):
    try:
        versionRes = requests.get(url)
        versionData = versionRes.json()
        jarUrl = versionData["downloads"]["client"]["url"]

        print(f'DOWNLOADING JAR FOR VER {versionData["id"]}')
        jarRes = requests.get(jarUrl)

        if not os.path.exists('./jars'):
            os.mkdir('./jars')   

        open(f'./jars/{versionData["id"]}.jar', 'wb').write(jarRes.content)

        print(f'Successfully downloaded jar file of {versionData["id"]}')
    except Exception as e:
        print(e)
        print("Something went wrong while downloading jar.")