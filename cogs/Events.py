import discord
from discord.ext import commands
from discord import Color

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel = guild.get_channel(876855680496193556)

        embed = discord.Embed(title="Welcome to the server!", description=f"{member} has joined SkyEvents. Head over to #events to start participating.", color=Color.gold())

        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text= "Made by enderelijas#5225")

        await channel.send(embed=embed)