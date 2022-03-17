from typing import Optional  # typing 문법

from fastapi import FastAPI  # fastapi 가져오기

app = FastAPI()

# @: 데코레이터 문법 : 함수를 꾸며주는 역할  -> @app.get을 라우터라고 부름
@app.get("/")  # 서버는 get+url을 통해 요청을 받고, return값으로 요청에 응답한다.
def read_root():
    print("helloworld")
    return {"Hello": "World"}


@app.get("/hello")
def read_fastapi_hello():
    print("helloworld")
    return {"Hello": "Fastapi"}


@app.get("/items/{item_id}/{xyz}")
def read_item(item_id: int, xyz=str, q: Optional[str] = None):
    return {"item_id": item_id, "q": q, "xyz": xyz}  # 입력 파라미터가 들어간다


# app.main::app --reload -> app/main.py/@app실행 (reload:코드가 변경되면 서버 재시작)
# 각 라우터별 기능과 반환을 수행한다.
