import os
import dice

import discord
from discord.ext import commands
from discord.ext.commands import bot
from dotenv import load_dotenv
from numpy.core.defchararray import strip

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_TEST = os.getenv("GUILD_TEST")

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)


@client.event
async def on_ready():
    await client.wait_until_ready()
    print("Ready!")


@bot.command(name="roll")
async def self(message, arg):
    result = dice.roll(arg)

    resultString = ""
    successes = 0

    for roll in result:
        resultString += ("[**" + str(roll) + "**] ")
        if roll > 3:
            successes += 1

    if successes != 1:
        successes = str(successes) + " successes!"
    else:
        successes = str(successes) + " success!"

    embed = discord.Embed(description=f"` {successes} ` ⟵  {strip(resultString)}", color=message.author.color)
    embed.set_author(name=f"{message.author} rolls {arg}!",
                     icon_url=message.author.avatar.url)

    await message.channel.send(embed=embed)


client.run(TOKEN)
