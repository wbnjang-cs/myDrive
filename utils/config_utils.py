import json
from pathlib import Path

def InitializeConfig():
    mainDir = Path(__file__).parent.parent
    configDir = mainDir / "config"
    configPath = configDir / "config.json"

    configDir.mkdir(exist_ok=True)

    if not configPath.exists():
        defaultSavePath = mainDir / "default_uploads"
        defaultSavePath.mkdir(exist_ok=True)

        defaultData = {
            "save path" : str(defaultSavePath)
        }

        with open(configPath, 'w') as f:
            json.dump(defaultData, f, indent=4)

    return configPath



    

