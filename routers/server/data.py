from datetime import datetime, timezone
from aiogram import Router, F, exceptions
from aiogram.types import CallbackQuery

from api import HetznerManager
from keys import PageCB, Pages, Actions, Keyboards, ServerUpdate
from language import MessageText

router = Router(name="server_menu")


@router.callback_query(
    PageCB.filter(
        (F.page.is_(Pages.SERVER)) & (F.action.in_([Actions.INFO, ServerUpdate.UPDATE]))
    )
)
async def server_data(
    callback: CallbackQuery,
    callback_data: PageCB,
    key: str | None,
    server_password: str | None = None,
):
    server = await HetznerManager.get_server(key, callback_data.server_id)
    try:
        emoji = {"starting": "🟡", "stopping": "🔴", "running": "🟢", "off": "🔴"}
        status_emoji = emoji.get(server.status, "⚪") if server.status else "⚪"
        await callback.message.edit_text(
            text=MessageText.SERVER_INFO.format(
                name=server.name,
                status=server.status,
                ipv4=server.public_net.ipv4.ip if server.public_net.ipv4 else "NO IPV4",
                ipv6=server.public_net.ipv6.ip if server.public_net.ipv6 else "NO IPV6",
                ram=server.server_type.memory,
                cpu=server.server_type.cores,
                created=server.created.strftime("%Y-%m-%d"),
                country=server.datacenter.location.country,
                city=server.datacenter.location.city,
                password=server_password or "*",
                image=server.image.name,
                status_emoji=status_emoji,
                created_day=(datetime.now(tz=timezone.utc) - server.created).days,
                disk=server.server_type.disk,
                traffic=round(
                    ((server.ingoing_traffic or 0) + (server.outgoing_traffic or 0))
                    / 1024**3,
                    3,
                ),
            ),
            reply_markup=Keyboards.edit_server(key, callback_data.server_id),
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.IS_UPDATED)
