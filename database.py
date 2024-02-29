from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path

# BASE_DIR = Path(__name__).parent

engine = create_async_engine(
    f"sqlite+aiosqlite:///database.db"
)

new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
