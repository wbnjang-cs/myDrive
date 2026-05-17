from fastapi import FastAPI, UploadFile, Depends
from pathlib import Path
from security import Verify_ID
from typing import Annotated
from utils import (
    SaveAndHashFile,
    UpdateSavePath,
    GetSavePath,
    Check_File_Name_Exists,
    CreateDirectory
)



#======== Code that runs on startup ==================================================================
app = FastAPI()
#====================================================================================================================================

@app.post("/uploadfile/")
def create_upload_file(userFiles: list[UploadFile], Authentication: Annotated[str, Depends(Verify_ID)], savePath: str=None):
    uploadedFiles = []
    failedFiles = []
    mainSavePath = GetSavePath()
    
    if savePath is None:
        savePath = mainSavePath
    else:
        savePath = mainSavePath / Path(savePath)

    for file in userFiles:
        fileName = file.filename
    
        #Quick Check if file with same name exists. If it does, don't save file and return
        if Check_File_Name_Exists(fileName):
            fileName = fileName + "(File with identical name already exists)"
            failedFiles.append(fileName)
            continue

        #Check if file successfully saves
        if SaveAndHashFile(file, savePath):
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


