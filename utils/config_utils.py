import json
from pathlib import Path
import uuid
from fastapi import HTTPException
import json

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

def UpdateSavePath(savePath: Path, configPath: Path) ->  None:
    """
    Name: UpdateSavePath

    Function description: 

        Will recieve a desired save path from user. If that save path exists,
        the config.json will be updated.
                
    Inputs:
        
        savePath:   A Path object that points to the directory the user wishes to save their
                    file backups. It is provided by the user.
        
        configPath:  A Path object that points to the config.json file

    Return value: None

    Errors accounted for:

        1. savePath does not exist

        2. configPath is incorrect/config.json does not exist
    """
    #If the path the user gave does not exist, raise an error
    if not savePath.exists():
        raise HTTPException(status_code=404, detail="That directory does not exist. Try again please.")

    #If configPath doesn't exist
    if configPath.exists():
        try:
            #loads data from config gile
            with open(configPath, "r") as configFile:
                data = json.load(configFile)
            
            #update the "save path" value in data
            data["save path"] = str(savePath.resolve())

            #overwrite the config file with updated contents
            with open(configPath, "w") as configFile:
                json.dump(data, configFile, indent=4)

        #If any part of writing to config file fails, raise an error
        except Exception as e:
            print(f"failed to save path: {e}")
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    else:
        print("Config File can't be found. Please restart app.")
        raise HTTPException(status_code=500, detail="Config File can't be found")
#End of CheckPathAndUpdate =========================================================================================================
    

    
def GetSavePath(configPath: Path) -> Path:
    """
    Name: GetSavePath

    Function description:

        Will return the save path saved in the config.json folder
                
    Assumptions: the inputted configPath parameter correctly points to the config.json file

    Inputs: 
        configPath: a Path object that points to the config.json file

    Return value: 
        savePath: A Path that is the save path saved inside the config.json folder

    """
    with open(configPath, "r") as configFile:
        data = json.load(configFile)
    
    savePath = data["save path"]
    if savePath == None:
        raise HTTPException(status_code=400, detail="A save directory has not been set yet. Please choose a save directory before trying again.")

    return Path(savePath)
#End of GetSavePath ========================================================================================================================
