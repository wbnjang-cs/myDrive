from fastapi import UploadFile
from hashlib import sha256
from pathlib import Path
from .db_utils import Add_File, GetDBPath
import tempfile
from .config_utils import GetSavePath





def SaveAndHashFile(file: UploadFile) -> bool:
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
    savePath: a Path object that points to the file inside save directory specified in myDrive/config/config.json

    Return value:
        True : The file was successfully saved and added to DB

        False : The file failed to save to destination and DB
    """
    readAmount = 4
    tempName = None

    savePath = GetSavePath() / file.filename
    dbPath = GetDBPath()

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
                contentBytes = file.file.read(1024 * 1024 * readAmount)
                if not contentBytes:
                    break

                #feed hasher one mb at a time
                fileHasher.update(contentBytes)

                #write to the temp file one mb at a time
                tempFile.write(contentBytes)
        

        fileByteHash = fileHasher.hexdigest()

        #If file is succesfully added to DB, make real file point to temp file
        if Add_File(file.filename, fileByteHash):
            Path(tempName).replace(savePath)
            return True

        #If file failed to upload to DB, delete temp file and return False
        else:
            if tempName and Path(tempName).is_file():
                Path(tempName).unlink()
            return False

        
    
    #If error happens midway through process, delete temp file
    except Exception as e:
        if tempName and Path(tempName).is_file():
            Path(tempName).unlink()
        
        print(f"Upload failed: error type {e}")

        return False

    finally:
        # Crucial: Always close the incoming file stream
        file.file.close()
    
#End of SaveAndHashFile==============================================================================================

def CreateDirectory(dirStr: str) -> Path:
    """
    Name: CheckDirectory

    Function description: 
        Recieves a string that represents a directory we want to create inside the main save directory. 
        If it doesn't exist we create it, then return a Path object to the desired directory
                
    Assumptions: No assumptions

    Inputs: 
        dirStr: string of the directory we want to create

    Return value:
        dirPath: Path to directory we created
    """

    dirPath = Path(dirStr)
    mainSavePath = GetSavePath()
    dirPath = mainSavePath / dirPath
    dirPath.mkdir(exist_ok=True)

    return dirPath
    

    





            


