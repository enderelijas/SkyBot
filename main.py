import discord, os, aiohttp, json
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
    try:
        with open("data.json", 'r') as file:
            count = file.json()['count']
            client.count = count
    except IOError:
        print("File not found or damaged. Creating a new one.")

    print("Ready for events!")

@client.event
async def on_disconnect():
    with open("data.json", 'w') as file:
        count = Commands.CommandClass().get_count()
        data = {"count": count}

        file.write(json.dump(data))

client.run(BOT_TOKEN)