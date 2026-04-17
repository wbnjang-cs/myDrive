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
    #Finds the myDrive main folder
    mainDir = Path(__file__).parent.parent
    #Finds the myDrive/config directory
    configDir = mainDir / "config"
    #Finds the path to the config file located at myDrive/config/config.json
    configPath = configDir / "config.json"

    #If myDrive/config directory doesn't exist, makes it. If it does exist, continue
    configDir.mkdir(exist_ok=True)

    #If config file doesn't exist inside myDrive/config directory, make a default config file
    if not configPath.exists():
        #Find a path to a directory for default uploads at myDrive/default_uploads
        defaultSavePath = mainDir / "default_uploads"

        #Creates myDrive/default_uploads if it doesn't exist
        defaultSavePath.mkdir(exist_ok=True)

        #set the save path to myDrive/default_uploads
        defaultData = {
            "save path" : str(defaultSavePath)
        }

        # Creates the config file with the default save path saved at myDrive/config/config.json
        with open(configPath, 'w') as f:
            json.dump(defaultData, f, indent=4)

    return configPath
#End of InitializeConfig()=======================================================================================


    

