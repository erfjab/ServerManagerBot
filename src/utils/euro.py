import aiohttp


async def get_euro() -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(url="https://sarfe.erfjab.com/api/prices") as res:
            res.raise_for_status()
            data = await res.json()
            return int(data["eur1"])
