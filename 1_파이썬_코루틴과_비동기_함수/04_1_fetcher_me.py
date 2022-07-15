import asyncio
import requests
import time


def fetcher(session, url):
    with session.get(url) as response:
        return response.text


def main():

    urls = ["https://naver.com", "https://google.com", "https://instagram.com"] * 20

    """
    session = requests.Session()
    session.get(url)
    session.close()
    """

    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls]
        print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
