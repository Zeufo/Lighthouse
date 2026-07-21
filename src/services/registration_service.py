import time

from aiogram.types import Message
from loguru import logger

from database import AsyncSessionLocal, Users


class UserService:
    @staticmethod
    async def registrate(message: Message) -> None:
        async with AsyncSessionLocal() as session:
            logger.debug(f"new user is {message.chat.id} at {time.time()}")
            new_user = Users(user_id=message.chat.id, created_at=int(time.time()))
            session.add(new_user)
            await session.commit()
