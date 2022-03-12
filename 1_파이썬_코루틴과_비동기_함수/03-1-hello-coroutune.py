# https://docs.python.org/ko/3/library/asyncio-task.html

import asyncio


async def hellow_world():
    print("hello world")
    return 123


if __name__ == "__main__":
    asyncio.run(hellow_world())  # asyncio.run() : 코루틴 함수 실행
