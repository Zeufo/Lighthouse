import abc
import typing

table = str.maketrans("", "", ",./*-")


class Cleaner(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def clean() -> typing.Any:
        pass


class TelethonCleaner(Cleaner):
    @staticmethod
    async def clean() -> typing.Any:
        try:
            pass
        except Exception as e:
            pass
