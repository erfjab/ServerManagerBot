from aiogram import Router, F, exceptions
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from language import MessageText
from keys import Keyboards, ServerList, Actions
from api import HetznerAPI

router = Router(name="start")


@router.message(CommandStart(ignore_case=True))
async def start(message: Message):
    servers = await HetznerAPI.get_servers()

    if not servers:
        await message.answer(MessageText.NOT_FOUND)
        return

    await message.answer(MessageText.START, reply_markup=Keyboards.menu(servers))


@router.callback_query(ServerList.filter(F.action == Actions.HOME))
async def update_server_list(callback: CallbackQuery):
    servers = await HetznerAPI.get_servers()

    if not servers:
        return await callback.answer(MessageText.NOT_FOUND)

    try:
        await callback.message.edit_text(
            MessageText.START, reply_markup=Keyboards.menu(servers)
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.IS_UPDATED)
