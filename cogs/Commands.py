from discord.ext import commands
from methods import check_verification, get_uuid

class CommandClass(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = client.session
        self.hypixel_key = client.hypixel_key
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command()
    async def verify(self, ctx, username):
        session = self.session
        author = f"{ctx.author}#{ctx.author.discriminator}"
        uuid = (await get_uuid(session, username))
        verified = (await check_verification(session, ctx.author, uuid, self.hypixel_key))
        
        if (verified == True):
            await ctx.send("You have been verified!")
        else:
            await ctx.send("Something went wrong. Please try again later.")

    @commands.command()
    async def stop(self, client):
        await client.disconnect()
