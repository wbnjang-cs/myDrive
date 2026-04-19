from fastapi import FastAPI, UploadFile, HTTPException
from pathlib import Path
from utils import (
    SaveAndHashFile,
    UpdateSavePath,
    GetSavePath,
    Initialize_Database,
    InitializeConfig,
    Check_File_Name_Exists
)

#======== Code that runs on startup ==================================================================
dbPath = Initialize_Database()
configPath = InitializeConfig()
app = FastAPI()
#====================================================================================================================================

@app.post("/config/setPath")
def set_save_path (savePathName: str): 
    savePath = Path(savePathName)
    UpdateSavePath(savePath, configPath)

    return {"Message" : "Path successfully updated"}


@app.post("/uploadfile/")
def create_upload_file(file: UploadFile):
    fileName = file.filename
    
    #Quick Check if file with same name exists. If it does, don't save file and return
    if Check_File_Name_Exists(dbPath, fileName):
        raise HTTPException(status_code=409, detail="A file with the same name already exists")

    #File with matching name inside the save directory
    saveDir = Path(GetSavePath(configPath))
    savePath = saveDir / fileName

    #Saves the file to savePath and hashes the bytes using Sha256
    fileByteHash = SaveAndHashFile(file, savePath, dbPath)

    return {"filename" : fileName,
            "hash" : fileByteHash}

    