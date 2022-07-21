from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper

# from selfmade_book_scraper import scraper

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent  # 현재 파일의 부모노드로 경로설정
print(BASE_DIR)
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)  # return 값으로 json이 아닌 html로 하겠다는 의미의 파라미터
async def root(request: Request):  # Request 객체 : 요청하는 주체에 대한 정보를 담고 있는 하나의 객체

    # book = BookModel(keyword='파이썬',publisher='BJPublic',price = 1200,image = 'me.png')
    # print(await mongodb.engine.save(book))
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "지섭의 fast-api"}
    )  # id는 item.htmal로 전달
    # return을 html로 반환


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q
    # 1. 쿼리에서 검색어 추출
    # (예외처리)
    # - 검색어가 없다면 사용자에게 검색을 요구
    if not keyword:
        context = {"request": request, "title": "지섭의 fast-api", "keyword": keyword}
        return templates.TemplateResponse("./index.html", context)
    # - 검색어가 없다면 사용자에게 검색을 요구 return
    # - 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 보여준다 return
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집한다.

    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "./index.html",
            {
                "request": request,
                "title": "지섭의 fast-api",
                "books": books,
                "keyword": keyword,
            },
        )

    naver_book_scaraper = NaverBookScraper()
    books = await naver_book_scaraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["price"],
            image=book["image"],
        )
        book_models.append(book_model)
    # 3. DB에 수집된 데이터를 저장한다.
    await mongodb.engine.save_all(book_models)
    # - 수집된 각각의 데이터에 대해서 DB에 들어갈 모델 인스턴스를 찍는다.
    # - 각 모델 인스턴스를 DB에 저장한다.
    return templates.TemplateResponse(
        "./index.html", {"request": request, "books": books, "title": q, "keyword": q}
    )


@app.on_event("startup")
def on_app_start():  #
    print("hello server!")
    # client = AsyncIOMotorClient(MONGO_URL)
    # engine = AIOEngine(motor_client=client, database=MONGO_DB_NAME) # 여기서 서버를 열면 scope가 달라 다른 함수에서 사용하지 못하기 때문에 클래스를 정의하여 사용
    """before app starts"""
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    print("bye server!")
    """ after app shutdown"""
    # await mongodb.close()


# @app.get("/")  # 서버는 get+url을 통해 요청을 받고, return값으로 요청에 응답한다.
# def read_root():
#     print("helloworld")
#     return {"Hello": "World"}


# @app.get("/hello")
# def read_fastapi_hello():
#     print("helloworld")
#     return {"Hello": "Fastapi"}


# @app.get("/items/{item_id}/{xyz}")
# def read_item(item_id: int, xyz=str, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q, "xyz": xyz}  # 입력 파라미터가 들어간다


# app.main::app --reload -> app/main.py/@app실행 (reload:코드가 변경되면 서버 재시작)
# 각 라우터별 기능과 반환을 수행한다.
