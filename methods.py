import aiohttp, json

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