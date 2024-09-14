from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from utils.lang import MessageText
from utils.keys import server_list_keyboard
from utils.hetzner import HetznerManager

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    servers = await HetznerManager.get_servers(message.from_user.id)
    
    if not servers:
        await message.answer(MessageText.ServerNotFound)
        return

    await message.answer(
        MessageText.Start,
        reply_markup=server_list_keyboard(servers)
    )
