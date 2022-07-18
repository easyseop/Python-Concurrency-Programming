import asyncio
from tracemalloc import start
import aiohttp
import time
from odmantic import AIOEngine
from pathlib import Path

from config import get_secret
from models.book import BookModel
from models import mongodb


# from models import mongodb
# from models.book import BookModel


# def NaverBookScraper

# url =https://openapi.naver.com/v1/search/book?query=파이&page=1&display=2


async def fetch(session, url, i):

    print(i + 1, "번째 페이지")
    print(url)
    headers = {
        "X-Naver-Client-Id": get_secret("NAVER_API_ID"),
        "X-Naver-Client-Secret": get_secret("NAVER_API_SECRET"),
    }
    async with session.get(url, headers=headers) as response:
        link = await response.json()
        items = link["items"]
        return items


async def scraper():

    keyword = "파이썬"
    BASE_URL = f"https://openapi.naver.com/v1/search/book?query={keyword}&display=10"
    urls = [BASE_URL + f"&start={20*i+1}" for i in range(1, 5)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            *[fetch(session, url, i + 1) for i, url in enumerate(urls)]
        )


def start_scraper():
    mongodb.connect()
    asyncio.run(scraper())


start_scraper()
