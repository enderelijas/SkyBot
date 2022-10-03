import aiohttp

async def get_uuid(session, username):
    async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as response:
        uuid = await response.json()
        return uuid["id"]