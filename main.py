import logging
import os
from typing import Literal

import discord
import rolldice
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import database.connectionhandler as db

import formatting.embeds as msgs

load_dotenv("private.env")
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_TEST = os.getenv("GUILD_TEST")

load_dotenv("data.env")
STAGE = os.getenv("STAGE")
VERSION = os.getenv("VERSION")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

print(f"Launching UnownRoller {STAGE} {VERSION}...")


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_TEST))

    print(f"UnownRoller {STAGE} {VERSION} synced and running!")


availablecommands_help = Literal["help", "roll", "pokeroll", "core", "pokerole", "syntax", "beans"]


@tree.command(name="help", description="How to use UnownRoller", guild=discord.Object(id=GUILD_TEST))
async def _help(interaction, entry: availablecommands_help = None, public: bool = False):
    msg = "I don't know that command!"
    title = f"/help {entry}?"
    url = None

    match entry:
        case None:
            msg = "A dice-rolling tool that **lilyOS** (Leah#0004) made to ease playing Pokérole, a fan-made Pokémon " \
                  "TTRPG.\n\n" \
                  "Despite that, the command /roll can still be used to normally roll dice, independently of the " \
                  "Pokérole functionality.\n\n" \
                  "To get more information on Pokérole there is `/help entry pokerole`.\n" \
                  "For help on rolling dice, try `/help entry syntax`! "
            title = "This is UnownRoller!"
        case "roll":
            msg = "`dice` - Roll dice according to CritDice syntax\n" \
                  "`hidden` - Determines if only you or everyone can see the result"
            title = "/roll [dice] (hidden)"
        case "pokeroll":
            msg = "`dice` - Roll dice according to CritDice syntax\n" \
                  "`chancedice` - For move effects, chance dice are used. These only count successes when a 6 is rolled.\n" \
                  "`hidden` - Determines if only you or everyone can see the result"
            title = "/roll [dice] (hidden)"
        case "pokerole":
            msg = "It works exclusively off 6-sided dice (d6), counting successes if you roll above a 3 or in some cases only on 6.\n\n" \
                  "For basic rules regarding Pokérole, please consult the \"Resources\" section in the linked page.\n" \
                  "If you are getting started, I recommend p"
            title = "Pokérole is a fan-made TTRPG system in the Pokémon setting"
            url = "https://www.pokeroleproject.com/"
        case "syntax":
            msg = "`xDy` where x is an amount and y is the amount of sides the dice has.\n\n" \
                  "`3d6K2` with a `K` keeps the highest 2 rolls.\n" \
                  "`3d6k2` with a `k` keeps the lowest 2 rolls.\n\n" \
                  "All basic mathematical operations are also supported.\n" \
                  "`**` is exponential, `//` is floor division.\n\n" \
                  "For details, visit the linked page."
            title = "UnownRoller uses the CritDice syntax"
            url = "https://www.critdice.com/roll-advanced-dice/"

    await interaction.response.send_message(
        embed=msgs.botmsg(title, msg, url),
        ephemeral=not public)


# Simple package call + return
@tree.command(name="roll", description="Roll dice with CritDice syntax", guild=discord.Object(id=GUILD_TEST))
async def _roll(interaction, dice: str, public: bool = True):
    result, explanation = rolldice.roll_dice(dice)
    explanation = explanation.replace(",", ", ")

    await interaction.response.send_message(
        embed=msgs.rolls(dice, result, explanation, interaction.user),
        ephemeral=not public
    )


@tree.command(name="core", description="Grab information from the Pokérole book", guild=discord.Object(id=GUILD_TEST))
async def _core(interaction, page: str, public: bool = False):
    if page.isnumeric() and 0 < int(page) < 489:
        embed, file = msgs.imgmsg(f"Pokérole Core p{page}", f"res/corebook/{page}.jpeg")

        await interaction.response.send_message(
            embed=embed,
            file=file,
            ephemeral=not public)
    else:
        await interaction.response.send_message(
            embed=msgs.error(f"`{page}` is not a valid page number!", interaction.user.name),
            ephemeral=True
        )


@tree.command(name="pokeroll",
              description="Roll d6 with CritDice syntax, counting successes according to the Pokérole system",
              guild=discord.Object(id=GUILD_TEST))
async def _pokeroll(interaction, dice: str, chancedice: bool = False, public: bool = True):
    result, explanation = rolldice.roll_dice(dice)
    explanation = explanation.replace(",", ", ")

    # I could technically allow non-D6 rolls here, but this is for Pokérole, which only uses d6.
    if "d6" not in dice.replace(" ", "").lower():
        await interaction.response.send_message(
            embed=msgs.error("Not valid d6 rolls! (try `/syntax`)", interaction.user.name),
            ephemeral=True
        )

    else:
        # In Pokérole, 4/5/6 is a success.
        # If you are however rolling for status effects ("Chance Dice"), only a 6 is a success.
        successRolls = [6] if chancedice else [4, 5, 6]
        totalSuccesses = 0

        for success in successRolls:
            totalSuccesses += explanation.count(str(success))
            explanation = explanation.replace(str(success), f"**{success}**")

        # Add -es if plural is required
        if totalSuccesses == 1:
            result = f"{str(totalSuccesses)} success!"
        else:
            result = f"{str(totalSuccesses)} successes!"

        await interaction.response.send_message(
            embed=msgs.rolls(dice.replace("D", "d") + (" chance dice" if chancedice else ""), result,
                             explanation, interaction.user),
            ephemeral=not public
        )


# DATABASE LOOKUPS #
@tree.command(name="pokemon", description="Grab information about a Pokémon from UnownRoller's database",
              guild=discord.Object(id=GUILD_TEST))
async def _pokemon(interaction, id_name: str, public: bool = False):
    await interaction.response.send_message(
        embed=msgs.pkmndata(id_name),
        ephemeral=not public
    )


@tree.command(name="ability", description="Grab information about an ability from UnownRoller's database",
              guild=discord.Object(id=GUILD_TEST))
async def _pokemon(interaction, ability: str, public: bool = False):
    await interaction.response.send_message(
        embed=msgs.abilitydata(ability),
        ephemeral=not public
    )


@tree.command(name="move", description="Grab information about an ability from UnownRoller's database",
              guild=discord.Object(id=GUILD_TEST))
async def _pokemon(interaction, move: str, public: bool = False):
    await interaction.response.send_message(
        embed=msgs.movedata(move),
        ephemeral=not public
    )


# DATABASE MODIFICATION #
@commands.is_owner()
@tree.command(name="datamod-pokemon-add", description="Add data to list of Pokémon",
              guild=discord.Object(id=GUILD_TEST))
async def _datamod_pokemon_add(interaction, pokedex: int, page: int, rank: int, basehp: int, strength: str,
                               dexterity: str, vitality: str, special: str, insight: str, evolutionstage: str,
                               evolutionspeed: str, form: str = None):
    addresult = db.addpokemon(pokedex, page, rank, basehp, strength, dexterity, vitality, special, insight,
                              evolutionstage, evolutionspeed, form)

    if addresult == "success":
        await interaction.response.send_message(
            embed=msgs.pkmndata(pokedex),
            ephemeral=True)

    elif addresult.startswith("ability:"):
        await interaction.response.send_message(
            embed=msgs.error(f"Empty database entry created for {addresult.split(':')[1].title()}.",
                             "Adding an ability"),
            ephemeral=True
        )


@commands.is_owner()
@tree.command(name="datamod-pokemove", description="Modify and add data to list of Pokémon",
              guild=discord.Object(id=GUILD_TEST))
async def _datamod_pokemove(interaction, movename: str, rank: int):
    if db.hasperms(interaction.user.id) is True:
        pass
    else:
        logging.warning(f"{interaction.user} tried to modify pokemove data!")
        await interaction.response.send_message(
            embed=msgs.error("You do not have permission to change the database.", interaction.user.name),
            ephemeral=True
        )


@commands.is_owner()
@tree.command(name="datamod-ability", description="Modify and add data to list of Pokémon",
              guild=discord.Object(id=GUILD_TEST))
async def _datamod_ability(interaction, name: str, desc: str, effect: str):
    if db.hasperms(interaction.user.id) is True:
        pass
    else:
        logging.warning(f"{interaction.user} tried to modify pokemove data!")
        await interaction.response.send_message(
            embed=msgs.error("You do not have permission to change the database.", interaction.user.name),
            ephemeral=True
        )


client.run(TOKEN)
