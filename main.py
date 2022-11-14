import discord, os, aiohttp, json, sqlite3
from discord.ext import commands
from dotenv import load_dotenv
from cogs import Commands, Events, AdminCommands
from methods import convert_time

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
HYPIXEL_KEY = os.getenv('HYPIXEL_KEY')

client = commands.Bot(command_prefix="?", intents=discord.Intents().all())
client.session = aiohttp.ClientSession()

command_class = Commands.CommandClass(client)
admin_command_class = AdminCommands.AdminCommandClass(client)
event_class = Events.Events(client)


@client.event
async def on_ready():
    await client.add_cog(command_class)
    await client.add_cog(admin_command_class)
    await client.add_cog(event_class)
    await client.tree.sync()
    try:
        open("config.json")
    except IOError:
        print("Configuration file not found or damaged. Creating a new one.")
        with open("config.json", 'w') as file:
            data = {}

            json.dump(data, file)
            
    try:
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        cursor.execute("""CREATE TABLE users (
            user_id integer,
            xp integer, 
            level integer
            )""")
            
        db.commit()
        db.close()
    except sqlite3.OperationalError:
        pass
    print("Ready for events!")

client.run(BOT_TOKEN)