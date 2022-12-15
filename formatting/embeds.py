import discord


def rolls(roll: str, result: str, explanation: str, author: discord.User):
    embed = discord.Embed(description=f"` {result} ` ⟵  {explanation}", color=author.color)
    embed.set_author(name=f"{author} rolls {roll}!",
                     icon_url=author.avatar.url)

    return embed

def error(message: str, author: discord.User):
    embed = discord.Embed(description=f"{message}", color=0xff0000)
    embed.set_author(name=f"{author} caused an error!")

    return embed