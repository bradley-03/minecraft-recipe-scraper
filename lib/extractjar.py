import zipfile

def extract_jar (verName):
    try:
        with zipfile.ZipFile(f'./jars/{verName}.jar', 'r') as zip_ref:
            for member in zip_ref.namelist():
                if member.startswith("data/minecraft/recipe/"):
                    zip_ref.extract(member, './jars')
    except Exception as e:
        print(e)
        print("Something went wrong while extracting jar file.")