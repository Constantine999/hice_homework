from datetime import datetime

from sqlalchemy import Integer, text, UniqueConstraint, event, DDL
from sqlalchemy.orm import Mapped, mapped_column

from database import Base, engine

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


class Post(Base):
    __tablename__ = "posts"

    name: Mapped[str]
    text: Mapped[str]
    created: Mapped[datetime] = mapped_column(server_default=text("(DATETIME('now', 'utc'))"))
    sequence_number: Mapped[int] = mapped_column(primary_key=True)
    messages_count: Mapped[int] = mapped_column(Integer, server_default=text('0'))

    __table_args__ = (UniqueConstraint("name", "messages_count", name="unique_constraint"),)


event.listen(Post.__table__, "after_create", trigger)


async def create_models():
    """Создаёт таблицу"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
