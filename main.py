import os
import rolldice

import discord
from discord import app_commands
from dotenv import load_dotenv

import formatting.embeds

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_TEST = os.getenv("GUILD_TEST")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_TEST))
    print("Ready!")


@tree.command(name="roll", description="Roll dice as defined by CritDice syntax (See /syntax)", guild=discord.Object(
    id=GUILD_TEST))
async def _roll(interaction, diceroll: str):
    result, explanation = rolldice.roll_dice(diceroll)

    await interaction.response.send_message(
        embed=formatting.embeds.rolls(diceroll, result, explanation, interaction.user))


@tree.command(name="pokeroll", description="Roll d6 as defined by CritDice syntax and count successes (See /syntax)",
              guild=discord.Object(
                  id=GUILD_TEST))
async def _pokeroll(interaction, diceroll: str):
    result, explanation = rolldice.roll_dice(diceroll)

    if "d6" not in diceroll.replace(" ", ""):
        await interaction.response.send_message(
            embed=formatting.embeds.error("Not valid d6 rolls!", author=interaction.user)
        )

    else :
        await interaction.response.send_message(
            embed=formatting.embeds.rolls(diceroll, result, explanation, interaction.user)
        )



client.run(TOKEN)
