import abc
import typing

table = str.maketrans("", "", ",./*-")


class Cleaner(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def clean(*args, **kwargs) -> typing.Any:
        pass


class TelethonCleaner(Cleaner):
    @staticmethod
    async def clean(text: str) -> typing.Any:
        try:
            text.translate(table)
            return text
        except Exception as e:
            pass
