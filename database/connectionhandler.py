import json
import os
import sqlite3
from typing import Tuple

from dotwiz import DotWiz

import database.apicalls as api


def getcolumns(cur, table_name):
    sql = "select * from %s where 1=0;" % table_name
    cur.execute(sql)
    return [col[0] for col in cur.description]


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

    if len(responselist) == 0:
        return None

    conn.close()

    return responselist


def hasperms(id: int):
    return id in fetchvertical("authorizedusers")


def converttoinsert(dictionary: dict, table):
    columns = ", ".join(map(str, dictionary.keys()))
    values = ", ".join(map(str, dictionary.values()))

    statement = f"INSERT INTO {table} ({columns}) VALUES ({values})"

    return statement


def addability(name: str, description: str = None, effect: str = None):
    conn, cur = connect()

    dbstructure = {
        "name": f"'{name}'",
        "description": f"'{description}'" if description is not None else "null",
        "effect": f"'{effect}'" if effect is not None else "null"
    }

    cur.execute(converttoinsert(dbstructure, "abilities"))
    conn.commit()
    conn.close()


# :)
def addpokemon(pokedex: int, page: int, rank: int, basehp: int, strength: str, dexterity: str, vitality: str,
               special: str, insight: str, evolutionstage: str, evolutionspeed: str, form: str = None):
    conn, cur = connect()

    pokemondata = api.getpokemon(pokedex)
    speciesdata = api.getspecies(pokedex)

    if fetchhorizontal("abilities", "name", f"name = '{pokemondata.abilities[0].ability.name.lower()}'") is None:
        addability(pokemondata.abilities[0].ability.name.lower())
        return f"ability:{pokemondata.abilities[0].ability.name.lower()}"

    englishgenus = ""
    for genus in speciesdata.genera:
        if genus.language.name == "en":
            englishgenus = genus

    dbstructure = {
        "pokedex": pokedex,
        "name": f"'{pokemondata.name}'",
        "form": f"'{form}'" if form is not None else "''",
        "page": page,
        "rank": rank,
        "type1": f"'{pokemondata.types[0].type.name}'",
        "type2": f"'{pokemondata.types[1].type.name}'" if len(pokemondata.types) == 2 else "null",
        "ability1": f"'{pokemondata.abilities[0].ability.name.lower()}'",
        "ability2": f"'{pokemondata.abilities[1].ability.name.lower()}'" if len(pokemondata.abilities) == 2 and pokemondata.abilities[1].is_hidden is False else "null",
        "descriptor": f"'{englishgenus.genus}'",
        "hp": basehp,
        "str": strength.split(",")[0],
        "strmax": strength.split(",")[1],
        "dex": dexterity.split(",")[0],
        "dexmax": dexterity.split(",")[1],
        "vit": vitality.split(",")[0],
        "vitmax": vitality.split(",")[1],
        "spe": special.split(",")[0],
        "spemax": special.split(",")[1],
        "ins": insight.split(",")[0],
        "insmax": insight.split(",")[1],
        "evostage": f"'{evolutionstage}'",
        "evospeed": f"'{evolutionspeed}'",
        "weight": f"'{pokemondata.weight} kg'",
        "height": f"'{float(pokemondata.height) / 10} kg'",
    }

    cur.execute(converttoinsert(dbstructure, "pokemon"))
    conn.commit()
    conn.close()

    return "success"


def converttuple(tup):
    string = ''
    for item in tup:
        string = f"{string} {str(item)}"
    return string
