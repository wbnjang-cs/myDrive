import json
from pathlib import Path
import uuid
from fastapi import HTTPException


MAIN_DIR = Path(__file__).parent.parent

CONFIG_DIR = MAIN_DIR / "config"
CONFIG_DIR.mkdir(exist_ok=True)

CONFIG_PATH = CONFIG_DIR / "config.json"

def InitializeConfig() -> dict:
    """
    Name: InitializeConfig

    Function description: 

        First the function verifies if the myDrive/config directory exists. If it doesn't, it is created

        Next the function verifies if config.json is inside the directory. 
        If not, it is created with a default save path (myDrive/default_uploads)

    Inputs: None

    Return:

        data : The dictionary that is the contents of the json file
     """

    #If config file doesn't exist inside myDrive/config directory, make a default config file
    if not CONFIG_PATH.exists():
        #Find a path to a directory for default uploads at myDrive/default_uploads
        defaultSavePath = MAIN_DIR / "default_uploads"

        #Creates myDrive/default_uploads if it doesn't exist
        defaultSavePath.mkdir(exist_ok=True)

        #set the save path to myDrive/default_uploads
        data = {
            "save path" : str(defaultSavePath),
            "id" : str(uuid.uuid4())
        }
        # Creates the config file with the default save path saved at myDrive/config/config.json
        with open(CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        return data
        
    else:
        with open(CONFIG_PATH, "r") as configFile:
            data = json.load(configFile)
            return data

#End of InitializeConfig()=======================================================================================

_CONFIG_DATA = InitializeConfig()



def UpdateSavePath(savePath: Path) ->  None:
    """
    Name: UpdateSavePath

    Function description: 

        Will recieve a desired save path from user. If that save path exists,
        the config.json will be updated.
                
    Inputs:
        
        savePath:   A Path object that points to the directory the user wishes to save their
                    file backups. It is provided by the user.
    Return value: None

    Errors accounted for:

        1. savePath does not exist

        2. configPath is incorrect/config.json does not exist
    """
    #If the path the user gave does not exist, raise an error
    if not savePath.exists():
        print("UpdateSavePath : That directory does not exist. Try again please.")
        raise HTTPException(status_code=404, detail="That directory does not exist. Try again please.")

    if CONFIG_PATH.exists():
        try:
            resolvedPath = str(savePath.resolve())
            _CONFIG_DATA["save path"] = resolvedPath

            with open(CONFIG_PATH, 'w') as f:
                json.dump(_CONFIG_DATA, f, indent=4)
            
            _CONFIG_DATA = InitializeConfig()

        #If any part of writing to config file fails, raise an error
        except Exception as e:
            print(f"UpdateSavePath: failed to save path: {e}")
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    else:
        print("UpdateSavePath: Config File can't be found. Please restart app.")
        raise HTTPException(status_code=500, detail="Config File can't be found")
#End of CheckPathAndUpdate =========================================================================================================
    

    
def GetSavePath() -> Path:
    """
    Name: GetSavePath

    Function description:
        Will return the save path saved in the config.json folder
                
    Return value: 
        savePath: A Path that is the save path saved inside the config.json folder

    """
    

    return Path(_CONFIG_DATA["save path"])
#End of GetSavePath ========================================================================================================================

def GetID() -> str:
    """
    Name: GetID

    Function description:
        Will return the ID saved in the config.json folder
        
    Return value: 
        currID: The int that is the unique ID of this program

    """

    return _CONFIG_DATA["id"]
#End of GetSavePath ========================================================================================================================
