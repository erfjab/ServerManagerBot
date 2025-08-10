from eiogram.types import BotCommand
from src.config import BOT, DP
from src.handlers import setup_handlers
from src.utils.state import DatabaseStorage


async def main():
    await BOT.delete_webhook()
    DP.storage = DatabaseStorage()
    DP.include_router(setup_handlers())
    await BOT.set_my_commands(
        commands=[
            BotCommand(command="/start", description="Start/Restart the bot"),
        ]
    )
    await DP.run_polling(interval=1.0, timeout=0)
