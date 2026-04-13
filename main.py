from fastapi import FastAPI, UploadFile
from pathlib import Path
from utils import (
    SaveAndHashFile,
    CheckPathAndUpdate,
    GetSavePath,
    Initialize_Database,
    InitializeConfig
)

#======== Code that runs on startup ==================================================================
dpPath = Initialize_Database()
configPath = InitializeConfig()
saveDir = Path(GetSavePath(configPath))
app = FastAPI()
#====================================================================================================================================

@app.post("/config/setPath")
def set_save_path (savePathName: str): 
    savePath = Path(savePathName)
    CheckPathAndUpdate(savePath, configPath)

    return {"Message" : "Path successfully updated"}


@app.post("/uploadfile/")
def create_upload_file(file: UploadFile):
    #File with matching name inside the save directory
    savePath = saveDir / file.filename

    #Function located in utils/saveandhash.py
    #function saves the file to savePath and hashes the bytes using Sha256
    fileByteHash = SaveAndHashFile(file, savePath)

    return {"filename" : file.filename,
            "hash" : fileByteHash}

    