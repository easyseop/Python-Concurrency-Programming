import time
import asyncio

# 비동기 함수 : 코드가 반드시 작성된 순서 그대로 실행되는 것이 아니다.


async def delivery(name, mealtime):
    print(f"{name}에게 배달 완료!")
    await asyncio.sleep(mealtime)
    print(f"{name} 식사 완료,{mealtime}시간 소요...")
    print(f"{name} 그릇 수거 완료")


async def main():
    await asyncio.gather(  # 함수를 동시에 처리한다
        delivery("A", 3),
        delivery("B", 3),
        delivery("C", 4),
    )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
