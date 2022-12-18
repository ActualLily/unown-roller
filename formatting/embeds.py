import math
import string
from typing import Union

import discord
from numpy.core.defchararray import isnumeric

import database.connectionhandler as db
import database.apicalls as api

from formatting import emoji as em

UNOWN_COLOR = 0x636363


def edit_distance(string1: str, string2: str):
    if len(string1) > len(string2):
        difference = len(string1) - len(string2)
        string1[:difference]

    elif len(string2) > len(string1):
        difference = len(string2) - len(string1)
        string2[:difference]

    else:
        difference = 0

    for i in range(len(string1)):
        if string1[i] != string2[i]:
            difference += 1

    return difference


def imgmsg(title: str, image: str):
    embed = discord.Embed(title=title,
                          color=UNOWN_COLOR)
    file = discord.File(image, filename="image.png")
    embed.set_image(url="attachment://image.png")
    return embed, file


def botmsg(title: str, text: str, url: str):
    embed = discord.Embed(title=title,
                          description=text,
                          color=0x636363,
                          url=url)
    return embed


def rolls(roll: str, result: str, explanation: str, author: discord.User):
    embed = discord.Embed(description=f"` {result} ` ⟵  {explanation}",
                          color=author.color)
    embed.set_author(name=f"{author} rolls {roll}!",
                     icon_url=author.avatar.url)
    return embed


def error(message: str, author: str):
    embed = discord.Embed(description=f"{message}",
                          color=0xff0000)
    embed.set_author(name=f"{author} caused an error!")
    return embed


def getbubbles(min: int, max: int):
    return f"[ {'●' * min}{'◌' * (max - min)}{' ' * (12 - min - (max - min))} ]"


def abilitydata(ability: str):
    data = db.fetchhorizontal("abilities", filter=f"name = '{ability.lower()}'")

    if data is None:

        correction = db.fetchvertical("abilities", "name")

        for name in correction:
            if edit_distance(name, ability.lower()) < 1:
                return error(
                    f"{ability} was not found. Did you mean `{name}`?",
                    f"{ability.title()}")

        for name in correction:
            if edit_distance(name, ability.lower()) < 2:
                return error(
                    f"{ability} was not found. Did you mean `{name}`?",
                    f"{ability.title()}")

        if not isnumeric(ability[0]):
            # 434 - 471 pages are abilities. Divide the alphabet over it equally to suggest a page
            alphabetposition = string.ascii_lowercase.index(ability[0].lower()) + 1
            possiblepage = math.floor(433 + (37 / 26) * alphabetposition)
            return error(
                f"{ability} was not found in the database.\nBased on alphabetic order, try `/core {possiblepage}`!",
                f"{ability.title()} not found!")
        else:
            return error(f"{ability} was not found in the database.\nDid you type it correctly?",
                         f"{ability.title()} not found!")

    embed = discord.Embed(description=data["description"])
    embed.set_author(name=ability.title())
    embed.set_footer(text=data["effect"])

    return embed


def pkmndata(pokemon: Union[int, str]):
    if isinstance(pokemon, str):
        filter = f"{'pokedex' if pokemon.isnumeric() else 'name'} = {int(pokemon) if pokemon.isnumeric() else pokemon}"
    else:
        filter = f"pokedex = {pokemon}"

    data = db.fetchhorizontal("pokemon", filter=filter)

    embed = discord.Embed(color=UNOWN_COLOR)
    embed.set_author(
        name=f"#{(3 - len(str(data['pokedex']))) * '0'}{data['pokedex']} - {data['name'].title()}, the {data['descriptor']}")
    embed.set_thumbnail(
        url=f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/{data['pokedex']}.png")

    embed.add_field(name="Stats",
                    value=f"`BHP {getbubbles(data['hp'], data['hp'])}`\n" +
                          f"` ------------------ `\n" +
                          f"`STR {getbubbles(data['str'], data['strmax'])}`\n" +
                          f"`DEX {getbubbles(data['dex'], data['dexmax'])}`\n" +
                          f"`VIT {getbubbles(data['vit'], data['vitmax'])}`\n" +
                          f"`SPE {getbubbles(data['spe'], data['spemax'])}`\n" +
                          f"`INS {getbubbles(data['ins'], data['insmax'])}`",
                    inline=True)

    # I forgot to capizalize the primary / foreign types in the database, and now I suffer
    embed.add_field(name="Traits",
                    value=f"**Type**\n" +
                          f"{data['type1'].title()}" + f"\n{data['type2'].title() if data['type2'] is not None else ''}\n\n" +
                          f"**Abilities**\n" +
                          f"{data['ability1'].title()}" + f"\n{data['ability2'].title() if data['ability2'] is not None else ''}",
                    inline=True)

    embed.add_field(name="Data",
                    value=f"**Weight:** {data['weight']}\n" +
                          f"**Height:** {data['height']}\n\n" +
                          f"**Stage:** {data['evostage']}\n" +
                          f"**Evolution:** {data['evospeed']}\n",
                    inline=True)

    embed.add_field(name="Moves",
                    value=f"{em.rankemoji(1)}this\n{em.rankemoji(2)}one\n{em.rankemoji(3)}is\n{em.rankemoji(4)}gonna\n{em.rankemoji(5)}be\n{em.rankemoji(6)}really\n{em.rankemoji(7)}tough\n",
                    inline=True)
    embed.add_field(name="Moves",
                    value=f"{em.rankemoji(1)}just\n{em.rankemoji(2)}make\n{em.rankemoji(3)}some\n{em.rankemoji(4)}kind\n{em.rankemoji(5)}of\n{em.rankemoji(6)}serializable\n{em.rankemoji(7)}json?\n",
                    inline=True)
    embed.add_field(name="Moves",
                    value=f"{em.rankemoji(1)}for\n{em.rankemoji(2)}now\n{em.rankemoji(3)}this\n{em.rankemoji(4)}is\n{em.rankemoji(5)}just\n{em.rankemoji(6)}test\n{em.rankemoji(7)}data\n",
                    inline=True)

    embed.set_footer(
        text=api.getrandomdex(pokemon)
    )

    return embed