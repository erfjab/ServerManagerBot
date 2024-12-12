from aiogram import Router, F, exceptions
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from language import MessageText
from keys import Keyboards, PageCB, Pages
from config import EnvFile

router = Router(name="start")


@router.message(CommandStart(ignore_case=True))
async def start(message: Message):
    await message.answer(
        MessageText.START, reply_markup=Keyboards.home(EnvFile.HETZNER_API_KEYS)
    )


@router.callback_query(PageCB.filter(F.page == Pages.HOME))
async def update(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            MessageText.START, reply_markup=Keyboards.home(EnvFile.HETZNER_API_KEYS)
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.IS_UPDATED)


@router.callback_query(PageCB.filter(F.page == Pages.MENU))
async def menu(callback: CallbackQuery, key: str | None):
    try:
        await callback.message.edit_text(
            MessageText.SERVER_LIST, reply_markup=Keyboards.menu(key)
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.IS_UPDATED)
