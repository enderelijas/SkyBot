import discord, json
from discord.ext import commands
from discord import Color
from methods import add_user, get_level, gain_xp, get_xp, level_up, check_user

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # welcoming the user
        guild = member.guild
        channel = guild.get_channel(876855680496193556)

        embed = discord.Embed(title="Welcome to the server!", description=f"{member} has joined SkyEvents. Head over to #events to start participating.", color=Color.gold())

        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text= "Made by enderelijas#5225")

        await channel.send(embed=embed)

        # adding user record to database
        await add_user(member)

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

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        channel = message.channel
        if (not user.bot):
            # making sure the user exists in the database, if not he gets added
            if (await check_user(user.id)):
                await gain_xp(user.id, 15)
                await level_up(message)
                
            else:
                await add_user(user)
                await gain_xp(user.id, 15)
            