import os
from typing import Literal

import discord
import rolldice
from discord import app_commands
from dotenv import load_dotenv

import formatting.embeds

load_dotenv("private.env")
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_TEST = os.getenv("GUILD_TEST")

load_dotenv("release.env")
STAGE = os.getenv("STAGE")
VERSION = os.getenv("VERSION")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

print(f"Launching UnownRoller {STAGE} {VERSION}...")


@client.event
async def on_ready():

    await tree.sync()

    print(f"UnownRoller {STAGE} {VERSION} synced and running!")


availableCommands = Literal["help", "roll", "pokeroll", "core", "pokerole", "syntax", "beans"]


@tree.command(name="help", description="How to use UnownRoller")
async def _help(interaction, entry: availableCommands = None, public: bool = False):
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
        embed=formatting.embeds.botmsg(title, msg, url),
        ephemeral=not public)


# Simple package call + return
@tree.command(name="roll", description="Roll dice with CritDice syntax")
async def _roll(interaction, dice: str, hidden: bool = False):
    result, explanation = rolldice.roll_dice(dice)
    explanation = explanation.replace(",", ", ")

    await interaction.response.send_message(
        embed=formatting.embeds.rolls(dice, result, explanation, interaction.user),
        ephemeral=hidden)


@tree.command(name="core", description="Grab information from the Pokérole book")
async def _core(interaction, page: str, public: bool = False):
    if page.isnumeric() and 0 < int(page) < 489:
        embed, file = formatting.embeds.imgmsg(f"Pokérole Core p{page}", f"res/corebook/{page}.jpeg")

        await interaction.response.send_message(
            embed=embed,
            file=file,
            ephemeral=public)
    else:
        await interaction.response.send_message(
            embed=formatting.embeds.error(f"`{page}` is not a valid page number!", interaction.user),
            ephemeral=True
        )


@tree.command(name="pokeroll",
              description="Roll d6 with CritDice syntax, counting successes according to the Pokérole system")
async def _pokeroll(interaction, dice: str, chancedice: bool = False, hidden: bool = False):
    result, explanation = rolldice.roll_dice(dice)
    explanation = explanation.replace(",", ", ")

    # I could technically allow non-D6 rolls here, but this is for Pokérole, which only uses d6.
    if "d6" not in dice.replace(" ", "").lower():
        await interaction.response.send_message(
            embed=formatting.embeds.error("Not valid d6 rolls! (try `/syntax`)", interaction.user),
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
            embed=formatting.embeds.rolls(dice.replace("D", "d") + (" chance dice" if chancedice else ""), result,
                                          explanation, interaction.user),
            ephemeral=hidden
        )


client.run(TOKEN)
