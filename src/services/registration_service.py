import time
from operator import index
from typing import Sequence

from aiogram.types import Message
from loguru import logger
from sqlalchemy import Row, delete, select
from sqlalchemy.dialects.postgresql import insert

from database import AsyncSessionLocal, Users


class UserService:
    @staticmethod
    async def registrate(message: Message) -> None:
        async with AsyncSessionLocal() as session:
            logger.debug(f"new user is {message.chat.id} at {int(time.time())}")
            stmt = insert(Users).values(user_id=message.chat.id, created_at=int(time.time()))
            stmt = stmt.on_conflict_do_nothing(index_elements=["user_id"])

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    async def get_all_users() -> Sequence[Row[tuple[int]]]:
        async with AsyncSessionLocal() as session:
            query = select(Users.user_id)
            result = await session.execute(query)
            return result.fetchall()

    @staticmethod
    async def delete_user(user_id: int) -> None:
        async with AsyncSessionLocal() as session:
            query = delete(Users).where(Users.user_id == user_id)
            await session.execute(query)
            await session.commit()
