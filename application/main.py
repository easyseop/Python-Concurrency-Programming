from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates
from pathlib import Path
from application.models.book import BookModel
from application.models import mongodb

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword="파이썬", publisher="BJPublic", price=1200, image="ma.png")
    print(await mongodb.engine.save(book))
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "콜렉터 북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):

    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "콜렉터 북북이", "keyword": q}
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
