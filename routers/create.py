from aiogram import Router, F
from aiogram.types import CallbackQuery

from keys import Keyboards, ServerTypeSelect
from language import MessageText
from api import HetznerAPI

router = Router(name="create")


@router.callback_query(ServerTypeSelect.filter(F.is_select.is_(False)))
async def show_server_types(callback: CallbackQuery):
    server_types = await HetznerAPI.get_server_types()

    if not server_types:
        return await callback.answer(MessageText.NOT_FOUND)

    return await callback.message.edit_text(
        text=MessageText.SELECT_SERVER_TYPE,
        reply_markup=Keyboards.server_types(server_types),
    )


@router.callback_query(ServerTypeSelect.filter(F.is_select.is_(True)))
async def select_server_types(callback: CallbackQuery):
    return await callback.answer("you selected")
