import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

CURRENT_FILE_PATH = Path(__file__).resolve()
SRC_DIR = next(p for p in CURRENT_FILE_PATH.parents if p.name == "src")
DOTENV_PATH = SRC_DIR.parent / ".env"


try:
    load_dotenv(DOTENV_PATH)

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_PASS")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASSWORD")

    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")

except Exception as e:
    logger.critical("cant load dotenv info", e)
    raise RuntimeError("cant load dotenv info")
