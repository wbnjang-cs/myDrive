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
            fileName TEXT NOT NULL,
            filePath TEXT NOT NULL,
            fileHash TEXT NOT NULL UNIQUE
            )""")

    conn.commit()
    conn.close()

    return dbPath

def Add_File():
    print("hi")