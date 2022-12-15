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


@tree.command(name="help", description="How to use UnownRoller", guild=discord.Object(
    id=GUILD_TEST))
async def _help(interaction, command: str = None):
    msg = "I don't know that command!"
    title = f"/help {command}?"
    url = None

    match command:
        case None:
            msg = "A dice-rolling tool that **lilyOS** (Leah#0004) made to ease playing Pokérole, a fan-made Pokémon " \
                  "TTRPG.\n\n" \
                  "Despite that, the command /roll can still be used to normally roll dice, independently of the " \
                  "Pokérole functionality.\n\n" \
                  "To get more information on Pokérole there is `/unown pokerole`.\n" \
                  "For help on rolling dice, try `/unown syntax`! "
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
        case "syntax":
            # TODO Syntax
            msg = "`xDy` where x is an amount and y is the amount of sides the dice has.\n\n" \
                  "Check the linked page for detailed syntax. This command will update later."
            title = "CritDice syntax"
            url = "https://www.critdice.com/roll-advanced-dice"

    await interaction.response.send_message(
        embed=formatting.embeds.botmsg(title, msg, url),
        ephemeral=True)


# Simple package call + return
@tree.command(name="roll", description="Roll dice with CritDice syntax", guild=discord.Object(
    id=GUILD_TEST))
async def _roll(interaction, dice: str, hidden: bool = False):
    result, explanation = rolldice.roll_dice(dice)
    explanation = explanation.replace(",", ", ")

    await interaction.response.send_message(
        embed=formatting.embeds.rolls(dice, result, explanation, interaction.user),
        ephemeral=hidden)


@tree.command(name="pokeroll", description="Roll d6 with CritDice syntax, counting successes according to the Pokérole system",
              guild=discord.Object(
                  id=GUILD_TEST))
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
            embed=formatting.embeds.rolls(dice.lower() + (" chance dice" if chancedice else ""), result,
                                          explanation, interaction.user),
            ephemeral=hidden
        )


client.run(TOKEN)
