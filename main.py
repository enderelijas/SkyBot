import discord, os, aiohttp
from discord.ext import commands
from dotenv import load_dotenv
from cogs import Commands, Events

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
HYPIXEL_KEY = os.getenv('HYPIXEL_KEY')

client = commands.Bot(command_prefix="?", intents=discord.Intents().all())
client.session = aiohttp.ClientSession()
client.hypixel_key = HYPIXEL_KEY
client.add_cog(Commands.CommandClass(client))
client.add_cog(Events.Events(client))

@client.event
async def on_ready():
    print("Ready for events!")

client.run(BOT_TOKEN)