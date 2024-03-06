# ---------------------------------Импорты-------------------------------------
import asyncio
import time
from multiprocessing import Process
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from sqlalchemy import DDL, Integer, UniqueConstraint, event, select, text
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# -------------------Настройка подключения к БД и параметры модели ------------
url = "sqlite+aiosqlite:///database.db"
engine = create_async_engine(url)
new_session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = (UniqueConstraint("name", "messages_count", name="unique_constraint"),)

    name: Mapped[str]
    text: Mapped[str]
    created: Mapped[datetime] = mapped_column(server_default=text("(DATETIME('now', 'utc'))"))
    sequence_number: Mapped[int] = mapped_column(primary_key=True)
    messages_count: Mapped[int] = mapped_column(Integer, server_default="0")


trigger = DDL(
    '''
        CREATE TRIGGER IF NOT EXISTS messages_count_autoincrement
        AFTER INSERT ON posts
        BEGIN
        UPDATE posts
        SET messages_count = (SELECT COUNT(*) FROM posts WHERE name = NEW.name)
        WHERE sequence_number = NEW.sequence_number;
        END;
    '''
)

event.listen(Post.__table__, "after_create", trigger)


async def create_models():
    """Создаёт таблицу"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# ----------------------------Схемы Pydantic-----------------------------------
class Info(BaseModel):
    name: str = Field(title="Имя отправителя")
    text: str = Field(title="Текст сообщения")


class ResponseInfo(Info):
    created: datetime = Field(title="Дата и время отправки")
    sequence_number: int = Field(title="Порядковый номер сообщения")
    messages_count: int = Field(title="Количество сообщений от текущего пользователя")


# ----------------------------Запрос в БД--------------------------------------

lock = asyncio.Lock()


async def add_client_in_db(data: Info) -> list[ResponseInfo]:
    async with lock:
        async with new_session() as session:
            session.add(Post(**data.model_dump()))
            await session.commit()
            stmt = select(Post).order_by(-Post.sequence_number).limit(10)
            result: Result = await session.execute(stmt)

            return [
                ResponseInfo.model_validate(post, from_attributes=True)
                for post in result.scalars().all()
            ]


# ----------------------------Запуск сервера FastAPI---------------------------
@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Создает таблицу в БД в момент запуска сервера"""
    await create_models()
    yield


PORTS = (9000, 10000, 11000,)
app = FastAPI(lifespan=lifespan)


@app.post("/api/v1/client/", response_model=list[ResponseInfo], status_code=status.HTTP_201_CREATED)
async def add_client(data: Info):
    """Эндпоинт на добавление имени отправителя и текста сообщения"""
    return await add_client_in_db(data)


def start_server(port: int) -> None:
    """Запускает сервер с отдельным портом"""
    uvicorn.run("DummyMessenger:app", port=port)


if __name__ == "__main__":
    for port in PORTS:
        time.sleep(1)
        Process(target=start_server, args=(port,)).start()
