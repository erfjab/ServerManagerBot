from datetime import datetime, timezone

from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import GetHetzner, ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.SNAPSHOT, task=TaskType.INFO), IgnoreStateFilter())
async def snapshots_info(callback_query: CallbackQuery, callback_data: BotCB, hetzner: GetHetzner, _: ClearState):
    snapshot = hetzner.images.get_by_id(int(callback_data.target))
    if not snapshot:
        return await callback_query.message.edit(text=Dialogs.SNAPSHOTS_NOT_FOUND)
    update = await callback_query.message.edit(
        text=Dialogs.SNAPSHOTS_INFO.format(
            name=snapshot.name or snapshot.description or "No Name",
            status=snapshot.status,
            size=round(snapshot.image_size, 3) if snapshot.image_size else "Unknown",
            created=snapshot.created.strftime("%Y-%m-%d"),
            created_day=(datetime.now(timezone.utc) - snapshot.created).days,
        ),
        reply_markup=BotKB.snapshots_update(snapshot=snapshot),
    )
    return await UserMessage.clear(update, keep_current=True)
