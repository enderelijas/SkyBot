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
client.count = 0

command_class = Commands.CommandClass(client)
event_class = Events.Events(client)

client.add_cog(command_class)
client.add_cog(event_class)

@client.event
async def on_ready():
    try:
        with open("data.json", 'r') as file:
            data = json.load(file)
            client.count = data['count']
    except IOError:
        print("File not found or damaged. Creating a new one.")
        with open("data.json", 'w') as file:
            count = 0
            data = {"count": count}

            file.write(json.dumps(data))

    print("Ready for events!")

client.run(BOT_TOKEN)

with open("data.json", 'r+') as file:
    count = event_class.get_count()
    print(count)
    data = json.load(file)
    data['count'] = count