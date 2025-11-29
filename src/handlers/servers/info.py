from datetime import datetime, timezone

from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import IgnoreStateFilter

from src.db import UserMessage
from src.lang import Dialogs
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.utils.depends import GetHetzner, ClearState
from src.utils.euro import get_euro

router = Router()


@router.callback_query(BotCB.filter(area=AreaType.SERVER, task=TaskType.INFO), IgnoreStateFilter())
async def servers_info(callback_query: CallbackQuery, callback_data: BotCB, hetzner: GetHetzner, _: ClearState):
    server = hetzner.servers.get_by_id(int(callback_data.target))
    if not server:
        return await callback_query.message.edit(text=Dialogs.SERVERS_NOT_FOUND)

    ingoing_gb = round(((server.ingoing_traffic or 0) / 1024**3), 3)
    outgoing_gb = round(((server.outgoing_traffic or 0) / 1024**3), 3)
    total_gb = round(ingoing_gb + outgoing_gb, 3)
    included_gb = round(((getattr(server, "included_traffic", 0) or 0) / 1024**3), 3)
    used_percent = round((outgoing_gb / included_gb * 100), 1) if included_gb else None

    prices = server.server_type.prices
    price_hourly = "➖"
    price_monthly = "➖"
    if prices:
        hourly = float(prices[0]["price_hourly"]["gross"])
        monthly = float(prices[0]["price_monthly"]["gross"])
        try:
            euro_rate = await get_euro()
            price_hourly = f"{hourly:.4f}€ [{hourly * euro_rate:,.0f}T]"
            price_monthly = f"{monthly:.2f}€ [{monthly * euro_rate:,.0f}T]"
        except Exception:
            price_hourly = f"{hourly:.4f}€"
            price_monthly = f"{monthly:.2f}€"

    text = Dialogs.SERVERS_INFO.format(
        name=server.name,
        status=server.status,
        ipv4=server.public_net.ipv4.ip if server.public_net.ipv4 else "➖",
        ipv6=server.public_net.ipv6.ip if server.public_net.ipv6 else "➖",
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
        traffic_in=ingoing_gb,
        traffic_out=outgoing_gb,
        traffic_total=total_gb,
        traffic_included=included_gb,
        traffic_used_percent=(used_percent if used_percent is not None else "➖"),
        traffic_billable=round(max(total_gb - included_gb, 0), 3) if included_gb else 0,
        price_hourly=price_hourly,
        price_monthly=price_monthly,
    )
    reply_markup = BotKB.servers_update(server=server)

    try:
        update = await callback_query.message.edit(text=text, reply_markup=reply_markup)
    except Exception:
        await callback_query.answer()
        return
    return await UserMessage.clear(update, keep_current=True)
