from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from app.models import mongodb
from pathlib import Path

from app.models.book import BookModel

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent  # 현재 파일의 부모노드로 경로설정

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword="파이썬", publisher="BJPublic", price=1200, image="me.png")
    print(await mongodb.engine.save(book))  # DB에 저장
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "seop's collector"}
    )  # id는 item.htmal로 전달
    # return을 html로 반환


@app.get("/search", response_class=HTMLResponse)
async def root(request: Request, q: str):
    print(q)
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "seop's collector", "keyword": q}
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
