import discord


def imgmsg(title: str, image: str):
    embed = discord.Embed(title=title)
    file = discord.File(image, filename="image.png")
    embed.set_image(url="attachment://image.png")
    return embed, file

def botmsg(title: str, text: str, url: str):
    embed = discord.Embed(title=title,
                          description=text,
                          color=0x636363,
                          url=url)
    return embed


def rolls(roll: str, result: str, explanation: str, author: discord.User):
    embed = discord.Embed(description=f"` {result} ` ⟵  {explanation}", color=author.color)
    embed.set_author(name=f"{author} rolls {roll}!",
                     icon_url=author.avatar.url)

    return embed


def error(message: str, author: discord.User):
    embed = discord.Embed(description=f"{message}", color=0xff0000)
    embed.set_author(name=f"{author} caused an error!")

    return embed
