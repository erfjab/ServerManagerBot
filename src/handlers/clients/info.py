from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage, Client, AsyncSession
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.CLIENT, task=TaskType.INFO), IgnoreStateFilter())
async def clients_info(callback_query: CallbackQuery, db: AsyncSession, state_data: dict, _: ClearState):
    client = await Client.get_by_id(db, state_data["client_id"])
    if not client:
        return await callback_query.answer(text=Dialogs.CLIENTS_NOT_FOUND, show_alert=True)
    update = await callback_query.message.edit(
        text=Dialogs.CLIENTS_INFO.format(secret=client.secret),
        reply_markup=BotKB.clients_update(client.id),
    )
    return await UserMessage.clear(update, keep_current=True)
