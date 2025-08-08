from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter
from eiogram.state import StateManager

from src.db import AsyncSession
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.CLIENT, task=TaskType.MENU), IgnoreStateFilter())
async def clients_menu(callback_query: CallbackQuery, callback_data: BotCB, db: AsyncSession, state: StateManager):
    if callback_data.target != 0:
        await state.upsert_context(db=db, client_id=callback_data.target)
    return await callback_query.message.edit(
        text=Dialogs.CLIENTS_MENU, reply_markup=BotKB.clients_menu(id=callback_data.target)
    )
