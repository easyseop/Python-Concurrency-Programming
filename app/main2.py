from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent  # 현재 파일의 부모노드로 경로설정
print(BASE_DIR)
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        "./item.html", {"request": request, "id": id, "data": "hello! fast api!!"}
    )  # id는 item.htmal로 전달
    # return을 html로 반환
