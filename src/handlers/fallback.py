import logging

from eiogram.types import Update
from src.config import DP
from src.db import UserMessage


@DP.fallback
async def fallback_handler(update: Update):
    logging.warning(f"Fallback handler triggered for update: {update}")
    if update.message:
        await UserMessage.add(update.message)
    if update.callback_query:
        return await update.callback_query.answer()
