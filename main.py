import os

import discord
import rolldice
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


# Simple package call + return
@tree.command(name="roll", description="Roll dice as defined by CritDice syntax (See /syntax)", guild=discord.Object(
    id=GUILD_TEST))
async def _roll(interaction, diceroll: str, hidden: bool = False):
    result, explanation = rolldice.roll_dice(diceroll)
    explanation = explanation.replace(",", ", ")

    await interaction.response.send_message(
        embed=formatting.embeds.rolls(diceroll, result, explanation, interaction.user),
        ephemeral=hidden)


@tree.command(name="pokeroll", description="Roll d6 as defined by CritDice syntax and count successes (See /syntax)",
              guild=discord.Object(
                  id=GUILD_TEST))
async def _pokeroll(interaction, diceroll: str, chancedice: bool = False, hidden: bool = False):
    result, explanation = rolldice.roll_dice(diceroll)
    explanation = explanation.replace(",", ", ")

    # I could technically allow non-D6 rolls here, but this is for Pokérole, which only uses d6.
    if "d6" not in diceroll.replace(" ", "").lower():
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
            embed=formatting.embeds.rolls(diceroll.lower() + (" chance dice" if chancedice else ""), result,
                                          explanation, interaction.user),
            ephemeral=hidden
        )


client.run(TOKEN)
