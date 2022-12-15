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
async def _roll(interaction, diceroll: str, hidden: bool = False):
    result, explanation = rolldice.roll_dice(diceroll)

    await interaction.response.send_message(
        embed=formatting.embeds.rolls(diceroll, result, explanation, interaction.user),
        ephemeral=hidden)


@tree.command(name="pokeroll", description="Roll d6 as defined by CritDice syntax and count successes (See /syntax)",
              guild=discord.Object(
                id=GUILD_TEST))
async def _pokeroll(interaction, diceroll: str, hidden: bool = False, status: bool = False):
    result, explanation = rolldice.roll_dice(diceroll)

    if "d6" not in diceroll.replace(" ", ""):
        await interaction.response.send_message(
            embed=formatting.embeds.error("Not valid d6 rolls! (try `/syntax`)", interaction.user),
            ephemeral=True
        )

    else:
        successRolls = [4, 5, 6]

        if (status):
            successRolls = 6

        totalSuccesses = 0

        for success in successRolls:
            totalSuccesses += explanation.count(str(success))
            explanation = explanation.replace(str(success), f"**{success}**")

        if totalSuccesses == 1:
            result = f"{str(totalSuccesses)} success!"
        else:
            result = f"{str(totalSuccesses)} successes!"

        await interaction.response.send_message(
            embed=formatting.embeds.rolls(diceroll, result, explanation, interaction.user),
            ephemeral=hidden
        )

client.run(TOKEN)
