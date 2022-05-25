import time
import aiohttp
import asyncio
import threading
import os


async def fetcher(session, url):
    print(f"{os.getpid()} process | {threading.get_ident()} url : {url} ")
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = ["https://naver.com", "https://apple.com", "http://google.com"] * 10

    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(*[fetcher(session, url) for url in urls])
        print(result)


if __name__ == "__main__":

    start = time.time()
    asyncio.run(main())
    end = time.time()
    print("learning time : ", end - start)
