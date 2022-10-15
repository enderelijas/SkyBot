import discord, json
from discord.ext import commands
from discord import Color

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.count = self.client.count

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        channel = guild.get_channel(876855680496193556)

        embed = discord.Embed(title="Welcome to the server!", description=f"{member} has joined SkyEvents. Head over to #events to start participating.", color=Color.gold())

        embed.set_thumbnail(url=guild.icon_url)
        embed.set_footer(text= "Made by enderelijas#5225")

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction = payload.emoji
        user = payload.member
        channel = payload.channel_id
        guild = self.client.get_guild(payload.guild_id)

        if (not user.bot):
            with open("config.json", 'r') as file:
                data = json.load(file)
                verification_reaction = data['verification_reaction']
                verification_channel = data['verification_channel']
                role = guild.get_role(data['role'])
            if ((verification_reaction == str(reaction)) and (verification_channel == channel)):
                await user.add_roles(role)

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     channel = message.channel
    #     client = self.client
    #     count = self.count

    #     if (channel == client.get_channel(802838284547784747)):
    #         count += 1
    #         await channel.send(count)
        