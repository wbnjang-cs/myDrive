from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from typing import List, Annotated
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

@app.post("/uploadfile/")
def create_upload_file(userFiles: list[UploadFile] = File(...)):
    uploadedFiles = []
    failedFiles = []

    for file in userFiles:
        fileName = file.filename
    
        #Quick Check if file with same name exists. If it does, don't save file and return
        if Check_File_Name_Exists(dbPath, fileName):
            failedFiles.append(fileName)
            continue

        #File with matching name inside the save directory
        saveDir = Path(GetSavePath(configPath))
        savePath = saveDir / fileName

        #Saves the file to savePath and hashes the bytes using Sha256
        if SaveAndHashFile(file, savePath, dbPath):
            uploadedFiles.append(fileName)
        else:
            failedFiles.append(fileName)

    return {"Message" : f"The file {uploadedFiles} succesfully uploaded, the files {failedFiles} did not upload"}


@app.post("/config/setPath")
def set_save_path (savePathName: str): 
    savePath = Path(savePathName)
    UpdateSavePath(savePath, configPath)

    return {"Message" : "Path successfully updated"}



