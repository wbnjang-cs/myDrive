from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path
from typing import List, Annotated
from utils import (
    SaveAndHashFile,
    UpdateSavePath,
    GetSavePath,
    Initialize_Database,
    InitializeConfig,
    Check_File_Name_Exists,
    CreateDirectory,
    GetDBPath
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
    saveDir = GetSavePath()
    dbPath = GetDBPath()

    for file in userFiles:
        fileName = file.filename
    
        #Quick Check if file with same name exists. If it does, don't save file and return
        if Check_File_Name_Exists(fileName):
            fileName = fileName + "(File with identical name already exists)"
            failedFiles.append(fileName)
            continue

        #File with matching name inside the save directory
        savePath = saveDir / fileName

        #Check if file successfully saves
        if SaveAndHashFile(file):
            uploadedFiles.append(fileName)
        else:
            fileName = fileName + "(File with identical content already saved)"
            failedFiles.append(fileName)

    return {"Message" : "Upload Completed",
            "File Counts" : {
                "Total" : len(userFiles),
                "Success" : len(uploadedFiles),
                "Failed" : len(failedFiles)
            },
            "Successfull_Uploads" : uploadedFiles,
            "Failed_Uploads" : failedFiles}


@app.post("/config/setPath")
def set_save_path (savePathName: str): 
    savePath = Path(savePathName)
    UpdateSavePath(savePath)

    return {"Message" : "Path successfully updated"}

@app.post("/config/createsubdirectory")
def CreateSubDirectory(directoryName: str):
    CreateDirectory(directoryName)

    return {"Message" : "subdirectory successfully created"}


