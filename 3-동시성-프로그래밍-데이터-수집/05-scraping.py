import aiohttp
import asyncio


async def fetch(session, url, i):
    print(i + 1)

    headers = {
        "X-Naver-Client-Id": "8nwA7S8i0gwxvv5e2kdu",
        "X-Naver-Client-Secret": "b_QKZbqf_c",
    }

    async with session.get(url, headers=headers) as response:
        result = await response.json()  # json으로 호출
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)


async def main():
    Base_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [f"{Base_URL}?query={keyword}&display=20&start={i}" for i in range(1, 10)]
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":
    asyncio.run(main())
