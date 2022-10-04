from discord.ext import commands
from main import HYPIXEL_KEY
from methods import check_verification, get_uuid

class CommandClass(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = self.client.session
        self.hypixel_key = self.client.hypixel_key
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def verify(self, ctx, username):
        uuid = (await get_uuid(session, username))
        verified = (await check_verification(session, ctx.author, username, HYPIXEL_KEY))

        if (verified == True):
            await ctx.send("You have been verified!")
        else:
            await ctx.send("Something went wrong. Please try again later.")
