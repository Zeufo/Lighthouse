from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from telethon.tl.types import channels

from config import DB_URL

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def close_db() -> None:
    await engine.dispose()


# TODO: how should we keep user preferences
class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    created_at: Mapped[int] = mapped_column(BigInteger, nullable=False)


class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[str] = mapped_column(nullable=False)
    channel_title: Mapped[str] = mapped_column(nullable=False)
    data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    views: Mapped[str] = mapped_column(nullable=False)
    published_at: Mapped[str] = mapped_column(nullable=False)


class Channels(Base):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    channel_title: Mapped[str] = mapped_column(nullable=False, unique=True)
    channel_status: Mapped[bool] = mapped_column(nullable=False)
    subscribers: Mapped[int] = mapped_column(nullable=False)
    last_parsed_at: Mapped[int] = mapped_column(BigInteger, nullable=False)
    last_updated_at: Mapped[int] = mapped_column(BigInteger, nullable=False)


class Digest(Base):
    __tablename__ = "digest"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    is_approved: Mapped[str] = mapped_column(nullable=False)
    admin_comment: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False)
