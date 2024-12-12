from aiogram import Router, F, exceptions
from aiogram.types import CallbackQuery

from api import HetznerManager
from keys import PageCB, Pages, Actions, Keyboards
from language import MessageText

router = Router(name="server_menu")


@router.callback_query(
    PageCB.filter((F.page.is_(Pages.SERVER)) & (F.action.is_(Actions.LIST)))
)
async def server_actions(callback: CallbackQuery, key: str | None):
    servers = await HetznerManager.get_servers(key)
    try:
        return await callback.message.edit_text(
            text=MessageText.SERVER_LIST,
            reply_markup=Keyboards.servers(key, servers or []),
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.IS_UPDATED)
