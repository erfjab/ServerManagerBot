from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter
from eiogram.state import StateManager

from src.db import AsyncSession, UserMessage, User
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.CLIENT, task=TaskType.MENU), IgnoreStateFilter())
async def clients_menu(
    callback_query: CallbackQuery, callback_data: BotCB, db: AsyncSession, state: StateManager, _: ClearState, dbuser: User
):
    if int(callback_data.target) != 0:
        await state.upsert_context(db=db, client_id=callback_data.target)
    if int(callback_data.target) not in dbuser.client_ids() and not dbuser.is_owner:
        return await callback_query.answer(text="Access Denied", show_alert=True)
    update = await callback_query.message.edit(
        text=Dialogs.CLIENTS_MENU, reply_markup=BotKB.clients_menu(id=callback_data.target)
    )
    return await UserMessage.clear(update, keep_current=True)
