import asyncio

from factory import create_telegram_client


class MainProcess:
    @staticmethod
    async def Preparation(self) -> None:
        client = create_client("session_name")

    @staticmethod
    async def Start(self) -> None:
        pass
