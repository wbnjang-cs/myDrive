from fastapi import FastAPI, UploadFile, HTTPException
from hashlib import sha256
from pathlib import Path
import tempfile
import json




def SaveAndHashFile(file: UploadFile, savePath: Path) -> str:
    """
    Name: SaveAndHashFile

    Function description: 
    Will read in the file 1mb at a time. Will simultaneously save the file
    to a temp file while hashing the file's contents using sha256.

    After reading the file, the tempfile will be turned into an permanent file
    with the appropriate name located at savePath (see Inputs).

    If the program crashes before completely reading the inputed file,
    it will delete the temp file and return an error.
                
    Assumptions: No assumptions

    Inputs: 
    file: an UploadFile object of the file the user is trying to upload
    savePath: a Path object that points to the save directory specified in myDrive/config/config.json

    Return value:
    fileByteHash: A string of the hash of the contents of file, hashed using sha256
    """
    
    tempName = None
    try:
        #Sha256 object that takes in mbs and hashes them
        fileHasher = sha256()
        
        #Create a temp file in the same folder as where we want our file to be saved
        with tempfile.NamedTemporaryFile(dir=savePath.parent, delete=False) as tempFile:
            #get name of temp file
            tempName = tempFile.name

            #loop will run until it can't read any more mb
            while True:
                #get one mb of content from the file. if the mb is empty, break
                contentOneMB = file.file.read(1024 * 1024)
                if not contentOneMB:
                    break

                #feed hasher one mb at a time
                fileHasher.update(contentOneMB)

                #write to the temp file one mb at a time
                tempFile.write(contentOneMB)
        
        #will make destinationDir/myFile point to our temp file. temp file is renamed to myFile
        #file.name returns the entire absolute path. Path(fileName) just turns it into a path object
        Path(tempName).replace(savePath)

        fileByteHash = fileHasher.hexdigest()

        return fileByteHash
    
    except Exception as e:
        if tempName and Path(tempName).exists():
            Path(tempName).unlink()
        
        print(f"Upload failed: error type {e}")

        raise e
    
#End of SaveAndHashFile==============================================================================================



def UpdateSavePath(savePath: Path, configPath: Path) ->  None:
    """
    Name: UpdateSavePath

    Function description: 

        Will recieve a desired save path from user. If that save path exists,
        the config.json will be updated.
                
    Inputs:
        
        savePath:   A Path object that points to the directory the user wishes to save their
                    file backups
        
        configPath:  A Path object that points to the config.json file

    Return value: None

    Errors accounted for:

        1. savePath does not exist

        2. configPath is incorrect/config.json does not exist
    """

    if not savePath.exists():
        raise HTTPException(status_code=404, detail="That directory does not exist. Try again please.")

    if configPath.exists():
        try:
            with open(configPath, "r") as configFile:
                data = json.load(configFile)
            
            data["save path"] = str(savePath.resolve())

            with open(configPath, "w") as configFile:
                json.dump(data, configFile, indent=4)

        except Exception as e:
            print(f"failed to save path: {e}")
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
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
            


