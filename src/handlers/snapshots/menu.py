from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import GetHetzner, ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.SNAPSHOT, task=TaskType.MENU), IgnoreStateFilter())
async def snapshots_menu(callback_query: CallbackQuery, hetzner: GetHetzner, _: ClearState):
    snapshots = hetzner.images.get_all(type="snapshot")
    update = await callback_query.message.edit(
        text=Dialogs.SNAPSHOTS_MENU, reply_markup=BotKB.snapshots_menu(snapshots=snapshots)
    )
    return await UserMessage.clear(update, keep_current=True)
