import sqlite3 as sql

DB_PATH = "/home/ubuntu/Desktop/flask_1/database/db.sqlite"


def createCursor():
    conn = sql.connect(DB_PATH)
    cursor = conn.cursor()
    return {'conn':conn, 'cursor':cursor}

def createDB():
    data = createCursor()
    conn = data['conn']
    cursor = data['cursor']
    cursor.execute(
        """
        CREATE TABLE lenguajes (
            id integer PRIMARY KEY,
            nombre text,
            ultima_version text,
            compilado numeric,
            lanzamiento text
        )
        """        
    )
    conn.commit()
    conn.close()

def addValues():
    data = createCursor()
    conn = data['conn']
    cursor = data['cursor']
    datos = [
        ("Java","12.1.2",1,"Agosto del 1990"),
        ("C++","3.9",0,"Septiembre del 1990"),
        ("JavaScript","11.1.2",0,"Enero del 1995"),
        ("PHP","5.1.2",1,"Febrero del 1991"),
        ("Kotlin","5.1.2",1,"Febrero del 1991"),
        ("Swift","5.1.2",1,"Febrero del 1991"),
    ]
    cursor.executemany(
        """
        INSERT INTO lenguajes VALUES(null,?,?,?,?)
        """,datos
    )
    conn.commit()
    conn.close()

if __name__ == "__main__":
    #createDB()
    addValues()
    print("DATOS CREADOS")
    