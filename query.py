import asyncio

from sqlalchemy import func, select
from sqlalchemy.engine import Result

from database import new_session
from schemas import Info, ResponseInfo
from src.models import Post

lock = asyncio.Lock()


async def add_client(data: Info) -> list[ResponseInfo]:
    async with lock:
        await asyncio.sleep(0.01)
        async with new_session() as session:
            total = await session.execute(select(func.count()).select_from(Post).where(Post.name == data.name))
            await asyncio.sleep(0)
            count_post = total.scalar()
            client = Post(**data.model_dump(), messages_count=count_post + 1)
            session.add(client)
            await session.commit()

            stmt = select(Post).order_by(-Post.sequence_number).limit(10)
            result: Result = await session.execute(stmt)
            return [
                ResponseInfo.model_validate(post, from_attributes=True)
                for post in result.scalars().all()
            ]
