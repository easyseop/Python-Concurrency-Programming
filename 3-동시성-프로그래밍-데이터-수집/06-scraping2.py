import aiohttp
import asyncio
import aiofiles
import os
from config import get_secret


async def img_downloader(session, img):
    img_name = img.split("/")[-1].split("?")[0]

    try:
        os.mkdir("./images")
    except FileExistsError:
        pass

    async with session.get(img) as response:
        if response.status == 200:
            async with aiofiles.open(f"./images/{img_name}", mode="wb") as file:
                img_data = await response.read()
                await file.write(img_data)


async def fetch(session, url, i):
    print(i + 1)

    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }

    async with session.get(url, headers=headers) as response:
        result = await response.json()  # json으로 호출
        items = result["items"]
        images = [item["image"] for item in items]
        print(images)

    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[img_downloader(session, img) for img in images])


async def main():
    Base_URL = "https://openapi.naver.com/v1/search/book"
    keyword = "파이썬"
    urls = [f"{Base_URL}?query={keyword}&display=20&start={20*i+1}" for i in range(5)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":
    asyncio.run(main())
