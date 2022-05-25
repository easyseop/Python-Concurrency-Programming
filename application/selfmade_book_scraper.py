import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
from config import get_secret
from models.book import BookModel
from models import mongodb


async def fetch(session, url, i):
    print(i + 1)

    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }

    async with session.get(url, headers=headers) as response:
        keyword, publisher, price, image = None, None, None, None

        result = await response.json()
        # json으로 호출
        items = result["items"]
        for i in items:

            keyword = i["title"]
            publisher = i["publisher"]
            price = i["price"]
            image = i["image"]
            book = BookModel(
                keyword=keyword, publisher=publisher, price=price, image=image
            )
            await mongodb.engine.save(book)


async def main():
    Base_URL = "https://openapi.naver.com/v1/search/book"
    keyword = "파이썬"
    urls = [f"{Base_URL}?query={keyword}&display=20&start={20*i+1}" for i in range(10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":

    mongodb.connect()
    asyncio.get_event_loop().run_until_complete(main())
    mongodb.close()
