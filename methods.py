import aiohttp, json, discord, sqlite3
from datetime import timedelta

db = sqlite3.connect("data.db")
cursor = db.cursor()

async def get_uuid(session, username):
    async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as response:
        uuid = await response.json()
        return uuid["id"]

async def check_verification(session, author, uuid, key):
    async with session.get(f"https://api.hypixel.net/player?uuid={uuid}&key={key}") as response:
        response_json = await response.json()
        if (response_json['success'] == True):
            linked_discord = response_json['player']['socialMedia']['links']['DISCORD']
            if (str(author) == linked_discord):
                return True
            else:
                return False
        else:
            return False

async def set_config(*args):
    with open("config.json", 'r') as file:
        data = json.load(file)
        for arg in args:
            for key in arg:
                data[key] = arg[key]
    
    with open("config.json", 'w') as file:
        json.dump(data, file, indent=4)

async def check_user(user_id):
    exists = cursor.execute("SELECT EXISTS (SELECT * from users WHERE user_id = ?)", (user_id, )).fetchone()[0]

    if (exists == 1):
        return True
    else:
        return False

async def get_level(user_id):
    cursor.execute("SELECT level from users WHERE user_id = ?", (user_id, ))
    level = cursor.fetchone()

    return(level[0])

async def get_xp(user_id):
    cursor.execute("select xp from users where user_id = ?", (user_id, ))
    xp = cursor.fetchone()
    
    return(xp[0])

async def add_user(member):
    cursor.execute("insert into users values (?, ?, ?)", (member.id, 0, 0))

    db.commit()

async def remove_user(member):
    sql = "delete from users where user_id = %s"
    val = (member.id, )
    cursor.execute(sql, val)

    db.commit()

async def gain_xp(member_id, xp_amount):
    user_id = member_id

    level = await get_level(user_id)
    xp = await get_xp(user_id)

    cursor.execute("UPDATE users SET xp = ? where user_id = ?", (xp + xp_amount, user_id))
    
    db.commit()

async def level_up(message):
    user_id = message.author.id
    user = message.author

    level = await get_level(user_id)
    xp = await get_xp(user_id)
    xp_required = 5 * (level ** 2) + (50 * level) + 100 

    if xp >= xp_required:
        cursor.execute("UPDATE users SET level = ? WHERE user_id = ?", ((level + 1), message.author.id))

        db.commit()

        with open("config.json", 'r') as file:
            data = json.load(file)
            role_id = data.get(str(level + 1))
            if (role_id):
                role = user.guild.get_role(role_id)
                await user.add_roles(role)
        
        await message.channel.send(f"Congrats {user.mention} you leveled up to level " + str(level + 1))

async def wipe(user_id):
    cursor.execute("update users set level = 0, xp = 0 where user_id = ?", (user_id, ))

    db.commit()

async def convert_time(time):
    UNITS = {'s': "seconds", 'm': "minutes", 'h': "hours", 'd': "days"}
    count = int(time[:-1])
    unit = UNITS[time[-1]]
    
    return timedelta(**{unit: count})