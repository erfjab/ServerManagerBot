from .env import (
    DEBUG,
    SQLALCHEMY_DATABASE_URL,
    TELEGRAM_ADMINS_ID,
    TELEGRAM_API_TOKEN,
)
from .tg import BOT, DP

__all__ = [
    "DEBUG",
    "SQLALCHEMY_DATABASE_URL",
    "TELEGRAM_ADMINS_ID",
    "TELEGRAM_API_TOKEN",
    "BOT",
    "DP",
]
