from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.book_scraper import NaverBookScraper
from fastapi.templating import Jinja2Templates

from app.models import mongodb
from pathlib import Path

from app.models.book import BookModel

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent  # 현재 파일의 부모노드로 경로설정

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # book = BookModel(keyword="파이썬", publisher="BJPublic", price=1200, image="me.png")
    # print(await mongodb.engine.save(book))  # DB에 저장
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "seop's collector"}
    )  # id는 item.htmal로 전달
    # return을 html로 반환


@app.get("/search", response_class=HTMLResponse)
async def root(request: Request, q: str):
    # 1. 쿼리에서 검색어 추출
    keyword = q
    # (예외처리)
    # - 검색어가 없다면 사용자에게 검색을 요구 return

    if not keyword:
        context = {"request": request, "title": "지섭지섭"}
        return templates.TemplateResponse("./index.html", context)
    # - 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 보여준다

    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "./index.html", {"request": request, "title": "지섭지섭", "books": books}
        )
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집한다
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["price"],
            image=book["image"],
        )
        book_models.append(book_model)

    # 3. DB에 수집된 데이터를 저장한다
    await mongodb.engine.save_all(book_models)  # asyncoid.gather의 원리

    return templates.TemplateResponse(
        "./index.html",
        {"request": request, "title": "seop's collector", "books": books},
    )


@app.on_event("startup")
def on_app_start():

    """before app starts"""
    # await mongodb.connect
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
    """after app shutdown"""
