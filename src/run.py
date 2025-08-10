import logging
from copy import deepcopy

from uvicorn import Config, Server
from uvicorn.config import LOGGING_CONFIG
from eiogram.types import BotCommand

from src.config import (
    UVICORN_SSL_CERTFILE,
    UVICORN_SSL_KEYFILE,
    UVICORN_HOST,
    UVICORN_PORT,
    BOT,
    DP,
    TELEGRAM_WEBHOOK_HOST,
    TELEGRAM_WEBHOOK_SECRET_KEY,
)
from src.api import API
from src.handlers import setup_handlers
from src.utils.state import DatabaseStorage

logger = logging.getLogger(__name__)


def get_log_config():
    log_config = deepcopy(LOGGING_CONFIG)
    default_fmt = "[%(asctime)s] %(levelprefix)s %(message)s"
    date_fmt = "%m/%d %H:%M:%S"
    log_config["formatters"]["default"]["fmt"] = default_fmt
    log_config["formatters"]["default"]["datefmt"] = date_fmt
    log_config["formatters"]["access"]["fmt"] = default_fmt
    log_config["formatters"]["access"]["datefmt"] = date_fmt
    return log_config


async def main():
    logger.info("Starting bot server...")
    cfg = Config(
        app=API,
        host=UVICORN_HOST,
        port=UVICORN_PORT,
        workers=1,
        log_config=get_log_config(),
    )
    logger.info("Configuring SSL if provided...")
    if UVICORN_SSL_CERTFILE and UVICORN_SSL_KEYFILE:
        cfg.ssl_certfile = UVICORN_SSL_CERTFILE
        cfg.ssl_keyfile = UVICORN_SSL_KEYFILE
    logger.info(f"Initializing bot... [{TELEGRAM_WEBHOOK_HOST}]")
    await BOT.set_webhook(
        url=f"{TELEGRAM_WEBHOOK_HOST}/api/telegram/webhook",
        secret_token=TELEGRAM_WEBHOOK_SECRET_KEY,
        allowed_updates=[
            "message",
            "callback_query",
        ],
    )
    DP.storage = DatabaseStorage()
    DP.include_router(setup_handlers())
    await BOT.set_my_commands(
        commands=[
            BotCommand(command="/start", description="Start/Restart the bot"),
        ]
    )
    logger.info("Starting server...")
    server = Server(cfg)
    logger.info("Server is running...")
    await server.serve()
