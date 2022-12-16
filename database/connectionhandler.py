import json
import os
import sqlite3
from typing import Tuple

import database.apicalls as api


def connect() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(os.path.join(path, "pokerole.db"))

    cur = conn.cursor()

    return conn, cur


def fetchunit(table: str, column: str = "*", filter: str = None):
    conn, cur = connect()
    if "*" not in column and "," not in column:
        # Return direct values instead of Tuples if twodimensional
        conn.row_factory = lambda cursor, row: row[0]
    else:
        conn.row_factory = sqlite3.Row

    statement = f"SELECT {column} FROM {table}"
    if filter is not None:
        statement += f" WHERE {filter}"
    response = cur.execute(statement).fetchone()

    responsearray = dict(zip([seq[0] for seq in cur.description], response))

    conn.close()

    return responsearray


def fetchdata(table: str, column: str = "*", filter: str = None):
    conn, cur = connect()
    if "*" not in column and "," not in column:
        # Return direct values instead of Tuples if twodimensional
        conn.row_factory = lambda cursor, row: row[0]

    statement = f"SELECT {column} FROM {table}"
    if filter is not None:
        statement += f" WHERE {filter}"
    response = cur.execute(statement).fetchall()

    responsearray = dict(zip([seq[0] for seq in cur.description], [seq[0] for seq in response]))

    conn.close()

    return responsearray


def hasperms(id: int):
    if id in fetchdata("authorizedusers").values():
        return True
    else:
        return False


def adjustpokemon(pokedex, page, rank, hp, dex, vit, spe, ins, evolutionstage, evolutionspeed, form):
    conn, cur = connect()

    # we need to fetch data from the API before we can commit it as we don't want to make too frequent API calls
    # by requesting data for every command requesting Pokémon
    pkmn = api.getpokemon(pokedex)
    spc = api.getspecies(pokedex)

    print("test")
    return None


def convertTuple(tup):
    # initialize an empty string
    string = ''
    for item in tup:
        string = f"{string} {str(item)}"
    return string