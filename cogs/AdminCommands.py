import discord
from discord.ext import commands
from methods import wipe, set_config, convert_time
from datetime import datetime, timedelta

class AdminCommandClass(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def wipe(self, ctx, user: discord.User):
        await wipe(user.id)
        await ctx.send(f"User: {user.mention} has been wiped.")

    @commands.hybrid_group()
    @commands.has_permissions(administrator = True)
    async def setup(self, ctx):
        if (ctx.invoked_subcommand is None):
            await ctx.send("Invalid setup command...")

    @setup.command(name="verify", description="Sets the up the verification system")
    async def verify(self, ctx, channel: discord.TextChannel, reaction, role: discord.Role):

        data = {"verification_channel": channel.id, "verification_reaction": reaction, "role": role.id}

        await set_config(data)
            
        await ctx.send(f"Selected channel: <#{channel.id}>\nSelected emoji: {reaction}\nRole: {role.mention}")
        msg = await ctx.bot.get_channel(channel.id).send("React to this message to get verified.")
        await msg.add_reaction(reaction)

    @setup.command(name="add_level_role", description="Adds a levelling role")
    async def add_level_role(self, ctx, role: discord.Role, level_required):
        data = {level_required: role.id}

        await set_config(data)
        await ctx.send("Role added.")

    @setup.command(name="welcome", description="Sets the welcome channel")
    async def welcome(self, ctx, channel: discord.TextChannel):

        await set_config({"welcome_channel": channel.id})
      
        await ctx.send(f"Selected channel: <#{channel.id}>")

    @commands.hybrid_command(name="ban", description="Bans a user")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        guild = ctx.guild
        user = ctx.message.author
        embed = discord.Embed(title='You have been banned', color=discord.Color.orange())
        embed.add_field(name='From:', value=guild.name, inline=False)
        embed.set_thumbnail(url=guild.icon)
        if reason:
            embed.add_field(name='For:', value=reason, inline=False)
        else: embed.add_field(name='For:', value='Unspecified', inline=False)
        embed.set_footer(text=f'Banned on: {datetime.now().strftime("%x")}', icon_url=user.display_avatar)

        await member.send(embed=embed)
        await member.ban(reason=reason)
        await ctx.send(f'{member} has been banned.')

    @commands.hybrid_command(name="kick", description="Kicks a user")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        guild = ctx.guild
        user = ctx.message.author
        embed = discord.Embed(title='You have been kicked', color=discord.Color.orange())
        embed.add_field(name='From', value=guild.name, inline=False)
        embed.set_thumbnail(url=guild.icon)
        if reason:
            embed.add_field(name='For', value=reason, inline=False)
        else: embed.add_field(name='For:', value='Unspecified', inline=False)
        embed.set_footer(text=f'Kicked on: {datetime.now().strftime("%x")}', icon_url=user.display_avatar)

        await member.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.send(f'{member} has been kicked.')

    @commands.hybrid_command(name="mute", description="Mutes a user")
    @commands.has_permissions(moderate_members = True)
    async def mute(self, ctx, member: discord.Member, duration, reason: str = None):
        guild = ctx.guild
        user = ctx.message.author
        embed = discord.Embed(title='You have been muted', color=discord.Color.orange())
        embed.add_field(name='In', value=guild.name, inline=False)
        embed.set_thumbnail(url=guild.icon)
        if reason:
            embed.add_field(name='For', value=reason, inline=False)
        else: embed.add_field(name='For:', value='Unspecified', inline=False)
        embed.set_footer(text=f'Muted on: {datetime.now().strftime("%x")}', icon_url=user.display_avatar)

        await member.send(embed=embed)

        await member.timeout(await convert_time(duration), reason=reason)
        await ctx.send(f'{member} has been muted.')

    