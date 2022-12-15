from typing import Any

import dice
import discord


def rolls(roll, *author):
    result = dice.roll(roll)

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

    if author is not None:
        embed = discord.Embed(description=f"` {successes} ` ⟵  {strip(resultString)}", color=message.author.color)
        embed.set_author(name=f"{author} rolls {roll}!",
                     icon_url=author.avatar.url)
    pass