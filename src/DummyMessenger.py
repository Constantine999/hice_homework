from contextlib import asynccontextmanager
from schemas import ResponseInfo, Info
import uvicorn
from fastapi import FastAPI, status

from src.models import create_models
import query


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_models()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/api/v1/", response_model=list[ResponseInfo], status_code=status.HTTP_201_CREATED)
async def add_client(data: Info):
    return await query.add_client(data)


if __name__ == "__main__":
    uvicorn.run("DummyMessenger:app", reload=True)
