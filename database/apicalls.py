import json
import logging
import random

import requests
from types import SimpleNamespace


def getrandomdex(pokemon: str):
    entries = []

    try:
        data = getspecies(pokemon)

        for entry in data.flavor_text_entries:
            entry.flavor_text = entry.flavor_text.replace("\n", " ").replace("\x0c", " ")
            if entry.language.name == "en" and entry.flavor_text not in entries:
                entries.append(entry.flavor_text)
    except:
        logging.warning(f"{pokemon} not found!")

    return entries[random.randrange(0, len(entries) - 1)]


def getpokemon(pokemon: str):
    pokemondata = ""

    try:
        request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
        pokemondata = json.loads(request.text, object_hook=lambda d: SimpleNamespace(**d))
        for pkmnability in pokemondata.abilities:
            pkmnability.ability.name = pkmnability.ability.name.replace('-', ' ')
    except:
        logging.warning(f"{pokemon} not found!")

    return pokemondata


def getspecies(pokemon: str):
    pokemondata = ""

    try:
        request = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{pokemon}")
        pokemondata = json.loads(request.text, object_hook=lambda d: SimpleNamespace(**d))
        print("")
    except:
        logging.warning(f"{pokemon} not found!")

    return pokemondata
