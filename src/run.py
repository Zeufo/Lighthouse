import asyncio

from database import PostgresInit


class MainProcess:
    @staticmethod
    async def Preparation() -> None:
        await PostgresInit.create()
        is_empty = await PostgresInit.is_empty()
        if is_empty:
            pass  # TODO: fill table class here

    @staticmethod
    async def Start(self) -> None:
        pass
