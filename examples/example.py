import asyncio

from spotify import Client


async def main():
    async with Client("id", "secret") as c:
        a = await c.get_album("id")
        print(a)

        for track in a:
            print(track)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
