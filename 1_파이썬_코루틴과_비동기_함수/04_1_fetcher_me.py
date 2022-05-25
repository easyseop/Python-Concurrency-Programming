import asyncio
import requests
import time


def fetch(session, url):
    with session.get(url) as response:
        return response.text


def main():
    urls = ["http://naver.com", "http://google.com", "http://instagram.com"] * 10

    with requests.Session() as session:
        result = [fetch(session, url) for url in urls]
        print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()

    print("learning time : ", end - start, "second")  # 12초
