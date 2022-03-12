# https://docs.aiohttp.org/en/stable/
# pip install aiohttp~=3.7.3


import time
import aiohttp
import asyncio


async def fetcher(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]

    """session = requests.Session()
    session.get(url) # file open과 비슷
    session.close()
    """

    async with aiohttp.ClientSession() as session:
        # result = [fetcher(session, url) for url in urls]
        # print(result)

        result = await asyncio.gather(
            *[fetcher(session, url) for url in urls]
        )  # *[] : unpacking -> 원소들이 쉼표 단위로 구분되어 인자로 전달
        # result = await fetcher( session, urls[0])
        # fetcher은 코루틴 함수이기에 어웨이터블 객체이고 await을 통하여 호출 되야 한다.

        print(result)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
