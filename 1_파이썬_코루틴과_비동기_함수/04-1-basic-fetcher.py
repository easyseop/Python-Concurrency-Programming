# https://2.python-requests.org/en/master/user/advanced/#id1
# pip install requests

import requests
import time


def fetcher(session, url):
    with session.get(url) as response:
        return response.text


def main():
    urls = ["https://naver.com", "https://google.com", "https://instagram.com"]

    """session = requests.Session()
    session.get(url) # file open과 비슷
    session.close() 
    """

    with requests.Session() as session:
        result = [fetcher(session, url) for url in urls] * 10
        print(result)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(end - start)
