from discord.ext import commands
from methods import get_uuid

class CommandClass(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = client.session
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def verify(self, ctx, username):
        session = self.session
        uuid = (await get_uuid(session, username))

        await ctx.send(uuid)
