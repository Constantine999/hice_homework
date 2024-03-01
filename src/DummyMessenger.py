from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status

import query
from schemas import Info, ResponseInfo
from src.models import create_models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """При запуске сервера создает автоматически не созданные таблицы"""
    await create_models()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/api/v1/", response_model=list[ResponseInfo], status_code=status.HTTP_201_CREATED)
async def add_client(data: Info):
    """Эндпоинт на добавление имени отправителя и текста сообщения"""
    return await query.add_client(data)


if __name__ == "__main__":
    uvicorn.run("DummyMessenger:app", reload=True)
