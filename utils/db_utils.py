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
    mainDir = Path(__file__).parent.parent
    dbDir = mainDir / "db"
    dbPath = dbDir / "files.db"

    dbDir.mkdir(exist_ok=True)

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