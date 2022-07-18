# https://docs.python.org/3.7/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
# aiohttp에서 제공하는 코루틴이 없다면 멀티 스레딩을 사용!

import requests
import time
import os
import threading
from concurrent.futures import ThreadPoolExecutor


def fetcher(params):
    session = params[0]
    url = params[1]
    print(f"{os.getpid()} process | {threading.get_ident()}")
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://apple.com", "http://google.com"] * 10

    executor = ThreadPoolExecutor(max_workers=10)

    with requests.Session() as session:
        params = [(session, url) for url in urls]
        print(params)
        result = list(executor.map(fetcher, params))
        # print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
