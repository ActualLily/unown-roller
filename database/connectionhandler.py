import json
import sqlite3


def initializedb():
    con = sqlite3.connect("pokerole.db")
    cur = con.cursor()

    types = ["fighting"]

    statement = f"INSERT INTO types VALUES('normal', '{json.dumps(types)}', NULL, NULL)"

    cur.execute(statement)
    con.commit()
    con.close()

initializedb()
