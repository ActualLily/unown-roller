import os
import sqlite3
from typing import Tuple

import database.apicalls as api


def connect() -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    path = os.path.dirname(os.path.realpath(__file__))
    conn = sqlite3.connect(os.path.join(path, "pokerole.db"))

    cur = conn.cursor()

    return conn, cur


def fetchhorizontal(table: str, column: str = "*", filter: str = None):
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

    if response is not None:
        response = dict(zip([seq[0] for seq in cur.description], response))

    conn.close()

    return response


def fetchvertical(table: str, column: str = "*", filter: str = None):
    conn, cur = connect()

    conn.row_factory = lambda cursor, row: row

    statement = f"SELECT {column} FROM {table}"
    if filter is not None:
        statement += f" WHERE {filter}"
    response = cur.execute(statement).fetchall()

    responselist = []

    for data in response:
        responselist.append(data[0])

    conn.close()

    return responselist


def hasperms(id: int):
    return id in fetchvertical("authorizedusers")


def adjustpokemon(pokedex, page, rank, hp, dex, vit, spe, ins, evolutionstage, evolutionspeed, form):
    conn, cur = connect()

    # we need to fetch data from the API before we can commit it as we don't want to make too frequent API calls
    # by requesting data for every command requesting Pokémon
    pkmn = api.getpokemon(pokedex)
    spc = api.getspecies(pokedex)

    print("test")
    return None


def converttuple(tup):
    string = ''
    for item in tup:
        string = f"{string} {str(item)}"
    return string
