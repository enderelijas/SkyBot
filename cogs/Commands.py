import discord, json
from discord.ext import commands
from methods import set_config, get_level

class CommandClass(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = client.session
    
    @commands.hybrid_command(name="ping", description="Pings the bot")
    async def ping(self, ctx):
        await ctx.send("Pong!")

    # @commands.command()
    # async def verify(self, ctx, username):
    #     session = self.session
    #     author = f"{ctx.author}#{ctx.author.discriminator}"
    #     uuid = (await get_uuid(session, username))
    #     verified = (await check_verification(session, ctx.author, uuid, self.hypixel_key))
        
    #     if (verified == True):
    #         await ctx.send("You have been verified!")
    #     else:
    #         await ctx.send("Something went wrong. Please try again later.")

    @commands.hybrid_command(name="level", description="Gets your level")
    async def level(self, ctx):
        user = ctx.message.author
        level = (await get_level(user.id))

        embed = discord.Embed(title=f'{user.name}\'s level', color=user.color)
        embed.add_field(name="Level: ", value=level)

        embed.set_thumbnail(url = user.display_avatar)
        await ctx.send(embed=embed)