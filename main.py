import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties

from middlewares import CheckAdminAccess
from routers import setup_routers
from utils import logger
from config import EnvFile


async def main() -> None:
    bot = Bot(
        token=EnvFile.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML, link_preview_is_disabled=True
        ),
    )
    dp = Dispatcher()

    dp.include_router(setup_routers())
    dp.update.middleware(CheckAdminAccess())

    try:
        bot_info = await bot.get_me()
        await bot.delete_webhook(True)
        logger.info("Polling messages for ServerManagerBot [@%s]...", bot_info.username)
        await dp.start_polling(bot)
    except (ConnectionError, TimeoutError, asyncio.TimeoutError) as conn_err:
        logger.error("Polling error (connection issue): %s", conn_err)
    except RuntimeError as runtime_err:
        logger.error("Runtime error during polling: %s", runtime_err)
    except asyncio.CancelledError:
        logger.warning("Polling was cancelled.")


if __name__ == "__main__":
    try:
        logger.info("Launching ServerManagerBot...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Bot stopped manually by user.")
    except RuntimeError as runtime_err:
        logger.error("Unexpected runtime error: %s", runtime_err)
    except (ConnectionError, TimeoutError, asyncio.TimeoutError) as conn_err:
        logger.error("Connection or timeout error: %s", conn_err)
    except asyncio.CancelledError:
        logger.warning("Polling was cancelled.")
