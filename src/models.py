from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, Integer

from database import Base, engine


class Post(Base):
    __tablename__ = "posts"

    name: Mapped[str]
    text: Mapped[str]
    created: Mapped[datetime] = mapped_column(server_default=text("(DATETIME('now', 'utc'))"))  # синтаксис SQLite
    # created: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))  # синтаксис PostgreSQL
    sequence_number: Mapped[int] = mapped_column(primary_key=True, unique=True)
    messages_count: Mapped[int] = mapped_column(Integer, default=0)


async def create_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
