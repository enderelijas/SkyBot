import discord, os, aiohttp
from discord.ext import commands
from dotenv import load_dotenv
from cogs import Commands, Events

client = commands.Bot(command_prefix="?", intents=discord.Intents().all())
client.session = aiohttp.ClientSession()
client.add_cog(Commands.CommandClass(client))
client.add_cog(Events.Events(client))
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

@client.event
async def on_ready():
    print("Ready for events!")

client.run(BOT_TOKEN)