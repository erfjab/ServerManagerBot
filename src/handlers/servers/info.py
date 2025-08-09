from datetime import datetime, timezone

from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import GetHetzner, ClearState

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.SERVER, task=TaskType.INFO), IgnoreStateFilter())
async def servers_info(callback_query: CallbackQuery, callback_data: BotCB, hetzner: GetHetzner, _: ClearState):
    server = hetzner.servers.get_by_id(int(callback_data.target))
    if not server:
        return await callback_query.message.edit(text=Dialogs.SERVERS_NOT_FOUND)

    update = await callback_query.message.edit(
        text=Dialogs.SERVERS_INFO.format(
            name=server.name,
            status=server.status,
            ipv4=server.public_net.ipv4.ip if server.public_net.ipv4 else "NO IPV4",
            ipv6=server.public_net.ipv6.ip if server.public_net.ipv6 else "NO IPV6",
            ram=server.server_type.memory,
            cpu=server.server_type.cores,
            created=server.created.strftime("%Y-%m-%d"),
            country=server.datacenter.location.country,
            city=server.datacenter.location.city,
            image=server.image.name or server.image.description,
            created_day=(datetime.now(tz=timezone.utc) - server.created).days,
            disk=server.server_type.disk,
            snapshot=len(
                [
                    snapshot
                    for snapshot in hetzner.images.get_all(type="snapshot")
                    if snapshot.created_from and snapshot.created_from.id == server.id
                ]
            ),
            traffic=round(
                ((server.ingoing_traffic or 0) + (server.outgoing_traffic or 0)) / 1024**3,
                3,
            ),
        ),
        reply_markup=BotKB.servers_update(server=server),
    )
    return await UserMessage.clear(update, keep_current=True)
