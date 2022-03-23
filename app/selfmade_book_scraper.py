import asyncio
from config2 import get_secret
import aiohttp
from models import mongodb
from models.book import BookModel


NAVER_API_BOOK = "https://openapi.naver.com/v1/search/book"


async def fetch(session, url):
    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }
    async with session.get(url, headers=headers) as response:
        result = await response.json()  # json으로 호출
        items = result["items"]
        # images = [item["link"] for item in items]
        title = [item["title"].replace("<b>", "").replace("</b>", "") for item in items]
        price = [item["price"] for item in items]
        publisher = [item["publisher"] for item in items]
        for t, p, q in zip(title, price, publisher):
            book = BookModel(keyword=t, publisher=q, price=int(p))
            print(t, p, q)
            await mongodb.engine.save(book)


async def main():
    Base_URL = "https://openapi.naver.com/v1/search/book"
    keyword = "파이썬"
    urls = [f"{Base_URL}?query={keyword}&display=20&start={20*i+1}" for i in range(5)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url) for url in urls])


# async def search(self, keyword, total_page):
#     apis = []


if __name__ == "__main__":
    mongodb.connect()
    asyncio.get_event_loop().run_until_complete(main())
    mongodb.close()
