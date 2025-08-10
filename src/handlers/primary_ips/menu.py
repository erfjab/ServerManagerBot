from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import GetHetzner, ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.PRIMARY_IP, task=TaskType.MENU), IgnoreStateFilter())
async def primary_ips(callback_query: CallbackQuery, hetzner: GetHetzner, _: ClearState):
    primary_ips = hetzner.primary_ips.get_all()
    update = await callback_query.message.edit(
        text=Dialogs.PRIMARY_IPS_MENU, reply_markup=BotKB.primary_ips_menu(primary_ips=primary_ips)
    )
    return await UserMessage.clear(update, keep_current=True)
