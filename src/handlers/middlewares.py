import logging
from typing import Any, Callable, Dict, Awaitable
from eiogram.middleware import BaseMiddleware
from eiogram.types import Update
from src.db import GetDB, User, UserMessage

logger = logging.getLogger(__name__)


class Middleware(BaseMiddleware):
    def __init__(self, priority: int = 0):
        super().__init__(priority)

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        update: Update,
        data: Dict[str, Any],
    ):
        async with GetDB() as db:
            user = update.origin.from_user
            dbuser = await User.upsert(db, user=user)
            if update.message:
                await UserMessage.add(update.message)
            if not dbuser.has_access:
                logger.warning(f"User {dbuser.id} try to access admin panel")
                return False
            data["dbuser"] = dbuser
            data["db"] = db
            return await handler(update, data)
