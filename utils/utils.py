from fastapi import UploadFile
from hashlib import sha256
from pathlib import Path
from .db_utils import Add_File
import tempfile





def SaveAndHashFile(file: UploadFile, savePath: Path, dbPath: Path) -> bool:
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

        fileByteHash = fileHasher.hexdigest()

        #If file is succesfully added to DB, replace the temp file with real file
        if Add_File(dbPath, file.filename, fileByteHash):
            Path(tempName).replace(savePath)

        #If file failed to upload to DB, delete temp file and return False
        else:
            if tempName and Path(tempName).exists():
                Path(tempName).unlink()
            return False

        return True
    
    #If error happens midway through process, delete temp file
    except Exception as e:
        if tempName and Path(tempName).exists():
            Path(tempName).unlink()
        
        print(f"Upload failed: error type {e}")

        return False
    
#End of SaveAndHashFile==============================================================================================







            


