from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from hcloud.servers.domain import Server
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.datacenters.domain import Datacenter

from .callback import ServerAction, ServerList, ServerTypeSelect, LocationTypeSelect, ImageTypeSelect
from .action import Actions
from language import KeyboardText


class KeyboardsCreater:
    def home(self):
        builder = InlineKeyboardBuilder()
        builder.button(
            text=KeyboardText.BACK, callback_data=ServerList(action=Actions.HOME).pack()
        )
        return builder.as_markup()

    def menu(self, servers: list[Server]):
        builder = InlineKeyboardBuilder()

        for server in servers:
            emoji = {"starting": "🟡", "stopping": "🔴", "running": "🟢", "off": "🔴"}
            status_emoji = emoji.get(server.status, "⚪")
            builder.button(
                text=f"{status_emoji} {server.name} ({server.public_net.ipv4.ip if server.public_net.ipv4 else 'No IPv4'})",
                callback_data=ServerAction(
                    action=Actions.INFO, server_id=server.id
                ).pack(),
            )

        builder.adjust(2)
        builder.row(
            InlineKeyboardButton(
                text=KeyboardText.UPDATE,
                callback_data=ServerList(action=Actions.HOME).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardText.CREATE, callback_data=LocationTypeSelect().pack()
            ),
        )

        return builder.as_markup()

    def edit_menu(self, serverid: int):
        builder = InlineKeyboardBuilder()

        actions = {
            Actions.POWER_ON: KeyboardText.POWER_ON,
            Actions.POWER_OFF: KeyboardText.POWER_OFF,
            Actions.REBOOT: KeyboardText.REBOOT,
            Actions.RESET_PASSWORD: KeyboardText.RESET_PASSWORD,
            Actions.DELETE: KeyboardText.DELETE,
            Actions.REBUILD: KeyboardText.REBUILD,
            Actions.UPDATE: KeyboardText.UPDATE_SERVER,
            Actions.RESET: KeyboardText.RESET,
        }

        for action, text in actions.items():
            builder.button(
                text=text,
                callback_data=ServerAction(action=action, server_id=serverid).pack(),
            )

        builder.button(
            text=KeyboardText.BACK, callback_data=ServerList(action=Actions.HOME).pack()
        )

        builder.adjust(2)
        return builder.as_markup()

    def confirm(self, action: str, serverid: int, imageid: int = 0):
        builder = InlineKeyboardBuilder()

        builder.button(
            text=KeyboardText.CONFIRM,
            callback_data=ServerAction(
                action=action,
                server_id=serverid,
                confirm=True,
                image_id=imageid,
            ).pack(),
        )
        builder.button(
            text=KeyboardText.CANCEL,
            callback_data=ServerAction(action=Actions.INFO, server_id=serverid).pack(),
        )

        builder.adjust(2)
        return builder.as_markup()

    def rebuild(self, images: list[Image], serverid: int):
        builder = InlineKeyboardBuilder()

        latest_images: dict[str, Image] = {}
        for image in images:
            if not image.name:
                continue
            if (
                image.name not in latest_images
                or image.created > latest_images[image.name].created
            ):
                latest_images[image.name] = image

        image_list: list[Image] = sorted(latest_images.values(), key=lambda x: x.name)

        for image in image_list:
            builder.button(
                text=image.name,
                callback_data=ServerAction(
                    action=Actions.REBUILD,
                    server_id=serverid,
                    confirm=False,
                    image_id=image.id,
                ).pack(),
            )

        builder.button(
            text=KeyboardText.CANCEL,
            callback_data=ServerAction(action=Actions.INFO, server_id=serverid).pack(),
        )

        builder.adjust(2)
        return builder.as_markup()

    def location_types(self, location_types: list[Datacenter]):
        builder = InlineKeyboardBuilder()

        for ser in location_types:
            builder.button(
                text=f"{ser.location.country}, {ser.location.city}",
                callback_data=LocationTypeSelect(
                    location=ser.id, is_select=True
                ).pack(),
            )

        builder.button(
            text=KeyboardText.CANCEL,
            callback_data=ServerList(action=Actions.HOME).pack(),
        )

        builder.adjust(1)
        return builder.as_markup()

    def server_types(self, server_types: list[ServerType]):
        builder = InlineKeyboardBuilder()

        for ser in server_types:
            builder.button(
                text=f"[{ser.architecture}] {ser.name} C:{ser.cores} M:{ser.memory} P:{ser.prices[0]['price_monthly']['net'][:5]}",
                callback_data=ServerTypeSelect(server=ser.id, is_select=True).pack(),
            )

        builder.button(
            text=KeyboardText.CANCEL,
            callback_data=ServerList(action=Actions.HOME).pack(),
        )

        builder.adjust(1)
        return builder.as_markup()

    def image_types(self, images: list[Image]):
        builder = InlineKeyboardBuilder()

        latest_images: dict[str, Image] = {}
        for image in images:
            if not image.name:
                continue
            if (
                image.name not in latest_images
                or image.created > latest_images[image.name].created
            ):
                latest_images[image.name] = image

        image_list: list[Image] = sorted(latest_images.values(), key=lambda x: x.name)

        for image in image_list:
            builder.button(
                text=image.name,
                callback_data=ImageTypeSelect(
                    image=image.id,
                    is_select=True
                ).pack(),
            )

        builder.button(
            text=KeyboardText.CANCEL,
            callback_data=ServerList(action=Actions.HOME).pack(),
        )

        builder.adjust(2)
        return builder.as_markup()
