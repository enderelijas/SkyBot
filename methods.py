import aiohttp

async def get_uuid(session, username):
    async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as response:
        uuid = await response.json()
        return uuid["id"]

async def check_verification(session, author, uuid, key):
    headers = {
        "Authorization": key
    }
    async with session.get("https://api.hypixel.net/player?uuid={uuid}") as response:
        linked_discord = response.json()['links']
        if (linked_discord):
            if (linked_discord == author):
                return True