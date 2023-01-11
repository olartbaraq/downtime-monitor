import asyncio
import aiohttp



async def main(url):

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, timeout=5) as response:
            print(dir(response))

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()
            print("Body:", html[:15], "...")

loop = asyncio.get_event_loop()
# loop.run_until_complete(main())