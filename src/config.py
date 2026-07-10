import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

CURRENT_FILE_PATH = Path(__file__).resolve()
SRC_DIR = next(p for p in CURRENT_FILE_PATH.parents if p.name == "src")
DOTENV_PATH = SRC_DIR.parent / ".env"


CHANNELS = [
    # RUS
    "@bazabaza",
    "@breakingmash",
    "@rbc_news",
    "@kommersant",
    "@rian_ru",
    "@ostorozhno_novosti",
    # EU
    "@bbcrussian",
    "@dwglavnoe",
    "@thebell_io",
    "@rtvi_news",
    "@euronews_ru",
    # ECO
    "@prostoecon",
    "@banksta",
    "@cb_economics",
    "@marketoverview",
    "@fatcat18",
    # IT & TECH
    "@koddurova",
    "@exploitex",
    "@addmeto",
    "@denis_sexy_it",
    "@tproger",
    "@dataleak",
    # CULT
    "@techinsiderru",
    "@postnauka",
    "@kinopoisk",
    "@art_of_it",
]


CHANNELS_BY_CATEGORY = {
    "RUS": [
        "@bazabaza",
        "@breakingmash",
        "@rbc_news",
        "@kommersant",
        "@rian_ru",
        "@ostorozhno_novosti",
    ],
    "EU": ["@bbcrussian", "@dwglavnoe", "@thebell_io", "@rtvi_news", "@euronews_ru"],
    "ECO": ["@prostoecon", "@banksta", "@cb_economics", "@marketoverview", "@fatcat18"],
    "IT_TECH": ["@koddurova", "@exploitex", "@addmeto", "@denis_sexy_it", "@tproger", "@dataleak"],
    "CULT": ["@techinsiderru", "@postnauka", "@kinopoisk", "@art_of_it"],
}


try:
    load_dotenv(DOTENV_PATH)

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASSWORD")

    DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    logger.debug(f"DB_URL: {repr(DB_URL)}")

    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    TEST_LINK = os.getenv("TEST_LINK")

    required_vars = {
        "DB_HOST": DB_HOST,
        "DB_PORT": DB_PORT,
        "DB_NAME": DB_NAME,
        "DB_USER": DB_USER,
        "DB_PASS": DB_PASS,
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "TEST_LINK": TEST_LINK,
    }

    for var_name, var_value in required_vars.items():
        if var_value is None:
            logger.critical(f"{var_name} is not set")
            raise RuntimeError
except Exception as e:
    logger.critical("cant load dotenv info", e)
    raise RuntimeError("cant load dotenv info")
