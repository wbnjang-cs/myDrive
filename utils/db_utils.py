import sqlite3
from pathlib import Path




def Initialize_Database() -> Path:
    """
    Name: Initialize_Database

    Function description: 
        If database already exists at myDrive/db/"dbname.db", 
        return that directory. Else create db at that location and then return

    Inputs: None

    Return value: 
        dbPath : A Path object that points to the db file
    """
    #Finds the myDrive main folder
    mainDir = Path(__file__).parent.parent
    #Finds the myDrive/db directory
    dbDir = mainDir / "db"
    #Finds the path to the db file located at myDrive/db/files.db
    dbPath = dbDir / "files.db"

    #If myDrive/db directory doesn't exist, makes it. If it does exist, continue
    dbDir.mkdir(exist_ok=True)

    #connect to the db file. If db file doesn't exist, make a new db file with a new table
    conn = sqlite3.connect(dbPath)

    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            fileName TEXT NOT NULL UNIQUE,
            fileHash TEXT NOT NULL UNIQUE
            )""")

    conn.commit()
    conn.close()

    return dbPath
#End of Initialize_Database ========================================================================================================================================




def Add_File(dbPath: Path, fileName: str, fileHash: str) -> bool:
    """
    Name: Add_File

    Function description: 
        Will add a file to the database, storing its name and hashed contents.
        Because the fileHash column is unique, if there is a duplicate
        trying to be uploaded the program will return an error.

    Inputs: 
            dbPath: a path object that points to the db file

            fileName: a str that is the name of the file

            fileHash: a str that is the sha256 hash of the file's contents

    Return value: 
            True : The file was succesfully added to db because it's contents were unique

            False : The file could not be added to the db, either because it was a duplicate
                    or because there was an error
    """
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    try:
        c.execute("""INSERT INTO files (fileName, fileHash) 
                    VALUES (?, ?) """,
                    (fileName, fileHash))
    
        conn.commit()
        return True
    
    except sqlite3.IntegrityError:
        print("That file already exists in the destination folder")
        return False
    except Exception as e:
        print(f"Error in uploading file: {e}")
        return False
    finally:
        conn.close()
#End of Add_File =======================================================================================================================



def Check_File_Name_Exists(dbPath: Path, fileName: str) -> bool:
    """
    Name: Check_File_Name_Exists

    Function description: 
        Will check the db to see if the fileName already exists

    Inputs: 
            dbPath: a path object that points to the db file

            fileName: a str that is the name of the file

    Return value: 
            True : The file already exists

            False : The file doesn't already exist, it is new
    """
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()

    try:
        c.execute("""SELECT * FROM files WHERE fileName=? """,
                  (fileName,))
        
        if c.fetchone() == None:
        
            return False
        else:
            return True
        
    except Exception as e:
        print(f"Failed to check database for duplicate: {e}")
        return True

    finally:
        conn.close()
#End of Check_File_Name_Exists =======================================================================================================================