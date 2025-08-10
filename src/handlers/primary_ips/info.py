from datetime import datetime, timezone

from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage
from src.lang import Dialogs
from src.keys import BotCB, BotKB, AreaType, TaskType
from src.utils.depends import GetHetzner, ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.PRIMARY_IP, task=TaskType.INFO), IgnoreStateFilter())
async def primary_ips_info(callback_query: CallbackQuery, callback_data: BotCB, hetzner: GetHetzner, _: ClearState):
    primary_ip = hetzner.primary_ips.get_by_id(int(callback_data.target))
    if not primary_ip:
        return await callback_query.message.edit(text=Dialogs.PRIMARY_IPS_NOT_FOUND)
    if primary_ip.assignee_id:
        server = hetzner.servers.get_by_id(primary_ip.assignee_id)
        if server:
            assignee = server.name
    update = await callback_query.message.edit(
        text=Dialogs.PRIMARY_IPS_INFO.format(
            name=primary_ip.name or "No Name",
            ip=primary_ip.ip,
            assignee=assignee if primary_ip.assignee_id else "No",
            assignee_id=primary_ip.assignee_id if primary_ip.assignee_id else "None",
            created=primary_ip.created.strftime("%Y-%m-%d"),
            created_day=(datetime.now(timezone.utc) - primary_ip.created).days,
        ),
        reply_markup=BotKB.primary_ips_update(primary_ip=primary_ip),
    )
    return await UserMessage.clear(update, keep_current=True)
