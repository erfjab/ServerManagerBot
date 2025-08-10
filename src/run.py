import logging

from eiogram.types import BotCommand

from src.config import BOT, DP, TELEGRAM_ADMINS_ID
from src.handlers import setup_handlers
from src.utils.state import DatabaseStorage


async def main():
    logging.info("Starting the bot...")
    await BOT.delete_webhook()
    logging.info("Webhook deleted, starting polling...")
    DP.storage = DatabaseStorage()
    logging.info("Dispatcher state storage initialized.")
    DP.include_router(setup_handlers())
    logging.info("Handlers set up successfully.")
    await BOT.set_my_commands(
        commands=[
            BotCommand(command="/start", description="Start/Restart the bot"),
        ]
    )
    logging.info("Bot commands set successfully.")
    logging.info(f"Admin IDs: {TELEGRAM_ADMINS_ID}")
    bot_data = await BOT.get_me()
    logging.info(f"Ready to start polling as @{bot_data.username} [{bot_data.full_name}]")
    await DP.run_polling(interval=1, timeout=1)
