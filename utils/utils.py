from fastapi import FastAPI, UploadFile, HTTPException
from hashlib import sha256
from pathlib import Path
import tempfile
import json

def SaveAndHashFile(file: UploadFile, savePath: Path):
    
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
                    break;

                #feed hasher one mb at a time
                fileHasher.update(contentOneMB)

                #write to the temp file one mb at a time
                tempFile.write(contentOneMB)
        
        #will make destinationDir/myFile point to our temp file. temp file is renamed to myFile
        #file.name returns the entire absolute path. Path(fileName) just turns it into a path object
        Path(tempName).replace(savePath)

        fileByteHash = fileHasher.hexdigest()
        #return dict, key is the string "filename", value is file.filename (file here is the paremeter)
        return fileByteHash
        #doesn't return an actual dict, returns this dict in the form of a json string
    
    except Exception as e:
        if tempName and Path(tempName).exists():
            Path(tempName).unlink()
        
        print(f"Upload failed: error type {e}")

        raise e
#End of SaveAndHashFile =========================================================================================================



def CheckPathAndUpdate(savePath: Path, configDir: Path):

    if not savePath.exists():
        raise HTTPException(status_code=404, detail="That directory does not exist. Try again please.")

    if configDir.exists():
        try:
            with open(configDir, "r") as configFile:
                data = json.load(configFile)
            
            data["save path"] = str(savePath.resolve())

            with open(configDir, "w") as configFile:
                json.dump(data, configFile, indent=4)

        except Exception as e:
            print(f"failed to save path: {e}")
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


#End of CheckPathAndUpdate =========================================================================================================


def GetSavePath(configDir: Path):
    with open(configDir, "r") as configFile:
        data = json.load(configFile)
    
    savePath = data["save path"]
    if savePath == None:
        raise HTTPException(status_code=400, detail="A save directory has not been set yet. Please choose a save directory before trying again.")

    return savePath
#End of GetSavePath ========================================================================================================================
            


