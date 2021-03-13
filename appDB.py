import sqlite3 

db = sqlite3.connect('todoDB.db')

def newClient():
    try:
        db.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS Client (
            clientname TEXT PRIMARY KEY,
            password TEXT,
            firstname TEXT,
            lastname TEXT
            );
            """
        )
        print("New ClientTable is created in database")
        db.commit()
    except:
        print("Failed creating ClientTable in database")
        db.rollback()


def newActivity():
    try:
        db.cursor().execute(
            """
            CREATE TABLE IF NOT EXISTS Activity (
            clientname TEXT,
            chores TEXT,
            finished TEXT,
            FOREIGN KEY(clientname) REFERENCES Client(clientname)
            );
            """
        )
        print("New ActivityTable is created in database")
        db.commit()
    except:
        print("Failed creating ActivityTable in database")
        db.rollback()
