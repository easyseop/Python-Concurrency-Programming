# https://docs.aiohttp.org/en/stable/
from bs4 import BeautifulSoup as bs
import aiohttp
import time
import asyncio


for i in range(1, 1 + 1):
    page_url = f"?page={i}"


async def fetch(session, url):
    async with session.get(url) as response:
        html = await response.text()
        soup = bs(html, "html.parser")
        cont_thumb = soup.find_all("div", "cont_thumb")
        for cont in cont_thumb:
            script = cont.find("p", "txt_thumb")
            if script is not None:
                print()
                print(script.text)


async def main():
    BASE_URL = "https://bjpublic.tistory.com/category/%EC%A0%84%EC%B2%B4%20%EC%B6%9C%EA%B0%84%20%EB%8F%84%EC%84%9C"
    urls = [f"{BASE_URL}?page={i}" for i in range(1, 1 + 1)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


if __name__ == "__main__":

    start = time.time()
    asyncio.run(main())
    end = time.time()
    print("learning time : ", end - start)
