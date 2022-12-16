import json
import logging
import requests
from types import SimpleNamespace


def getpokemon(pokemon: str):
    pokemondata = ""

    try:
        request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        pokemondata = json.loads(request.text, object_hook=lambda d: SimpleNamespace(**d))
    except:
        logging.warning(f"{pokemon} not found!")

    return pokemondata
