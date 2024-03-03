import asyncio

from sqlalchemy import func, select
from sqlalchemy.engine import Result

from database import new_session
from schemas import Info, ResponseInfo
from src.models import Post

lock = asyncio.Lock()


async def add_client(data: Info) -> list[ResponseInfo]:
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
