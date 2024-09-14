from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode


from config import ConfigManager
from routers import setup_routers
from middlewares.auth import CheckAdminAccess
from log import logger  


async def main():
    try:
        logger.warning('Starting config bot!')
        if not ConfigManager._load_config():
            return 
        
        bot = Bot(
            token=ConfigManager.get_bot_token(),
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )

        dp = Dispatcher()
        dp.include_router(setup_routers())
        dp.update.middleware(CheckAdminAccess())

        logger.info('Delete webhook messages')
        await bot.delete_webhook(True)
        logger.info('Starting Bot...')
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f'An aiogram error occurred: {str(e)}')


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())