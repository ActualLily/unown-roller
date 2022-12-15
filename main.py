import os
import rolldice

import discord
from discord import app_commands
from dotenv import load_dotenv
from numpy.core.defchararray import strip

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
async def rollcmd(interaction, diceroll: str):
    result, explanation = rolldice.roll_dice(diceroll)

    embed = discord.Embed(description=f"` {result} ` ⟵  {strip(explanation)}", color=interaction.user.color)
    embed.set_author(name=f"{interaction.user} rolls {diceroll}!",
                     icon_url=interaction.user.avatar.url)

    await interaction.response.send_message(embed=embed)


client.run(TOKEN)
