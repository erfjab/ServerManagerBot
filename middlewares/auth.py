from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Update
from utils import logger
from config import EnvFile


class CheckAdminAccess(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        user = None
        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
            key = event.callback_query.data.split(sep=":", maxsplit=2)[1]
            data["key"] = EnvFile.from_hash(hashkey=key) if key != "KEY" else None
        elif event.inline_query:
            user = event.inline_query.from_user

        if not user:
            logger.warning("Received update without user information!")
            return None

        if not EnvFile.is_admin(user.id):
            logger.warning(f"Blocked {user.username or user.first_name}")
            return None

        return await handler(event, data)
