import sqlite3
from pathlib import Path

def Initialize_Database():
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