import logging

from uvicorn import Config, Server
from eiogram.types import BotCommand

from src.api import API
from src.handlers import setup_handlers
from src.utils.state import DatabaseStorage
from src.config import (
    BOT,
    DP,
    UVICORN_SSL_CERTFILE,
    UVICORN_SSL_KEYFILE,
    UVICORN_HOST,
    UVICORN_PORT,
    TELEGRAM_WEBHOOK_HOST,
    TELEGRAM_WEBHOOK_SECRET_KEY,
)

logger = logging.getLogger(__name__)


async def main():
    cfg = Config(
        app=API,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        workers=1,
    )

    if UVICORN_SSL_CERTFILE and UVICORN_SSL_KEYFILE:
        cfg.ssl_certfile = UVICORN_SSL_CERTFILE
        cfg.ssl_keyfile = UVICORN_SSL_KEYFILE
        logger.info("SSL configuration loaded successfully")

    server = Server(cfg)
    logger.info(f"Starting server on {UVICORN_HOST}:{UVICORN_PORT}")
    await server.serve()


@API.on_event("startup")
async def startup_event():
    try:
        webhook_url = f"{TELEGRAM_WEBHOOK_HOST}/api/telegram/webhook"
        await BOT.set_webhook(
            url=webhook_url,
            secret_token=TELEGRAM_WEBHOOK_SECRET_KEY,
        )
        logger.info(f"Webhook successfully set up at {webhook_url}")
        DP.storage = DatabaseStorage()
        DP.include_router(setup_handlers())
        logger.info("All handlers initialized successfully")

        await BOT.set_my_commands(
            commands=[
                BotCommand(command="/start", description="Start or restart the bot"),
            ]
        )
        logger.info("Bot commands set up successfully")

        bot_data = await BOT.get_me()
        logger.info(
            f"Bot @{bot_data.username} is now running and ready to receive updates"
        )

    except Exception as e:
        logger.error(f"Startup failed: {str(e)}")
        raise
