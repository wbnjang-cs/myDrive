import json
from pathlib import Path

def InitializeConfig() -> Path:
    """
    Name: InitializeConfig

    Function description: 

        First the function verifies if the myDrive/config directory exists. If it doesn't, it is created

        Next the function verifies if config.json is inside the directory. 
        If not, it is created with a default save path (myDrive/default_uploads)

    Inputs: None

    Return value:
        configPath: a Path object that points to the config.json file.
     """
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
#End of InitializeConfig()=======================================================================================


    

