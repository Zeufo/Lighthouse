from sqlalchemy import JSON, BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from config import DB_URL

engine = create_async_engine(DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


# TODO: how should we keep user preferences
class User(Base):
    __tablename__ = "users"

    db_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False)


class News(Base):
    __tablename__ = "news"

    db_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(nullable=False)
