import requests
import time
import os
import threading


def fetcher(session, url):
    print(
        f"{os.getpid()} process | {threading.get_ident()} url : {url} "
    )  # os.getpid() : 현재 프로세스 ID 호출
    with session.get(url) as response:
        return response.text


def main():
    # urls = ["https://naver.com",
    # "https://google.com",
    #  "https://instagram.com"]
    urls = ["https://google.com"] * 50

    """session = requests.Session()
    session.get(url) # file open과 비슷
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
