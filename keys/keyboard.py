from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from hcloud.servers.domain import Server
from hcloud.images.domain import Image
from hcloud.server_types.domain import ServerType
from hcloud.datacenters.domain import Datacenter

from .callback import PageCB, SelectCB
from .enums import Actions, Pages, ServerCreate, ServerUpdate
from language import KeyboardText
from config import EnvFile


class KeyboardsCreater:
    def home(self, keys: list[list[str]]) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        for key in keys:
            builder.button(
                text=key[0],
                callback_data=PageCB(
                    key=EnvFile.to_hash(key[1]), page=Pages.MENU
                ).pack(),
            )

        builder.button(
            text=KeyboardText.UPDATE, callback_data=PageCB(page=Pages.HOME).pack()
        )
        return builder.adjust(1).as_markup()

    def menu(self, key: str) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
        builder.button(
            text=KeyboardText.SERVERS,
            callback_data=PageCB(
                key=hashkey, page=Pages.SERVER, action=Actions.LIST
            ).pack(),
        )
        builder.row(
            InlineKeyboardButton(
                text=KeyboardText.HOMES, callback_data=PageCB(page=Pages.HOME).pack()
            )
        )
        return builder.adjust(1).as_markup()

    def servers(self, key: str, servers: list[Server] = None) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
        for server in servers:
            emoji = {"starting": "🟡", "stopping": "🔴", "running": "🟢", "off": "🔴"}
            status_emoji = emoji.get(server.status, "⚪")
            builder.button(
                text=f"{status_emoji} {server.name} ({server.public_net.ipv4.ip if server.public_net.ipv4 else 'No IPv4'})",
                callback_data=PageCB(
                    key=hashkey,
                    page=Pages.SERVER,
                    action=Actions.INFO,
                    server_id=server.id,
                ).pack(),
            )

        builder.adjust(1)
        builder.row(
            InlineKeyboardButton(
                text=KeyboardText.UPDATE_SERVER,
                callback_data=PageCB(
                    key=hashkey, page=Pages.SERVER, action=Actions.LIST
                ).pack(),
            ),
            InlineKeyboardButton(
                text=KeyboardText.CREATE,
                callback_data=PageCB(
                    key=hashkey, page=Pages.SERVER, action=Actions.CREATE
                ).pack(),
            ),
        )
        builder.row(
            InlineKeyboardButton(
                text=KeyboardText.HOMES, callback_data=PageCB(page=Pages.HOME).pack()
            )
        )

        return builder.as_markup()

    def edit_server(self, key: str, serverid: int):
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
        actions = {
            ServerUpdate.POWER_ON: KeyboardText.POWER_ON,
            ServerUpdate.POWER_OFF: KeyboardText.POWER_OFF,
            ServerUpdate.REBOOT: KeyboardText.REBOOT,
            ServerUpdate.RESET_PASSWORD: KeyboardText.RESET_PASSWORD,
            ServerUpdate.DELETE: KeyboardText.DELETE,
            ServerUpdate.REBUILD: KeyboardText.REBUILD,
            ServerUpdate.RESET: KeyboardText.RESET,
            ServerUpdate.UPDATE: KeyboardText.UPDATE_SERVER,
        }

        for action, text in actions.items():
            builder.button(
                text=text,
                callback_data=PageCB(
                    key=hashkey, page=Pages.SERVER, action=action, server_id=serverid
                ).pack(),
            )

        builder.button(
            text=KeyboardText.SERVERS,
            callback_data=PageCB(
                key=hashkey, page=Pages.SERVER, action=Actions.LIST
            ).pack(),
        )

        builder.adjust(2)
        return builder.as_markup()

    def back_home(self) -> InlineKeyboardMarkup:
        builder = InlineKeyboardBuilder()
        builder.button(
            text=KeyboardText.UPDATE, callback_data=PageCB(page=Pages.HOME).pack()
        )
        return builder.adjust(1).as_markup()

    def confirm(self, key: str, action: str, serverid: int, imageid: int = 0):
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
        builder.button(
            text=KeyboardText.CONFIRM,
            callback_data=PageCB(
                key=hashkey,
                page=Pages.SERVER,
                action=action,
                server_id=serverid,
                image_id=imageid,
                confirm=True,
            ).pack(),
        )
        builder.button(
            text=KeyboardText.CANCEL,
            callback_data=PageCB(
                key=hashkey,
                page=Pages.SERVER,
                action=Actions.INFO,
                server_id=serverid,
                image_id=imageid,
            ).pack(),
        )

        builder.adjust(2)
        return builder.as_markup()

    def rebuild(self, key: str, images: list[Image], serverid: int):
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
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
                callback_data=PageCB(
                    key=hashkey,
                    page=Pages.SERVER,
                    action=ServerUpdate.REBUILD,
                    server_id=serverid,
                    confirm=False,
                    image_id=image.id,
                ).pack(),
            )

        builder.adjust(2)

        builder.row(
            InlineKeyboardButton(
                text=KeyboardText.CANCEL,
                callback_data=PageCB(
                    key=hashkey,
                    page=Pages.SERVER,
                    action=Actions.INFO,
                    server_id=serverid,
                ).pack(),
            )
        )
        return builder.as_markup()

    def location_types(self, key: str, location_types: list[Datacenter]):
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
        for ser in location_types:
            builder.button(
                text=f"{ser.location.country}, {ser.location.city}",
                callback_data=SelectCB(
                    key=hashkey,
                    page=Pages.SERVER,
                    action=Actions.CREATE,
                    datavalue=ser.id,
                    datatype=ServerCreate.LOCATION,
                ).pack(),
            )

        builder.button(
            text=KeyboardText.SERVERS,
            callback_data=PageCB(
                key=hashkey, page=Pages.SERVER, action=Actions.LIST
            ).pack(),
        )

        builder.adjust(1)
        return builder.as_markup()

    def server_types(self, key: str, server_types: list[ServerType]):
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
        for ser in server_types:
            builder.button(
                text=f"[{ser.architecture}] {ser.name} C:{ser.cores} M:{ser.memory} P:{ser.prices[0]['price_monthly']['net'][:5]}",
                callback_data=SelectCB(
                    key=hashkey,
                    page=Pages.SERVER,
                    action=Actions.CREATE,
                    datavalue=ser.id,
                    datatype=ServerCreate.SERVER,
                ).pack(),
            )

        builder.button(
            text=KeyboardText.SERVERS,
            callback_data=PageCB(
                key=hashkey, page=Pages.SERVER, action=Actions.LIST
            ).pack(),
        )
        builder.adjust(1)
        return builder.as_markup()

    def image_types(self, key: str, images: list[Image]):
        builder = InlineKeyboardBuilder()
        hashkey = EnvFile.to_hash(key)
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
                callback_data=SelectCB(
                    key=hashkey,
                    page=Pages.SERVER,
                    action=Actions.CREATE,
                    datavalue=image.id,
                    datatype=ServerCreate.IMAGE,
                ).pack(),
            )

        builder.adjust(2)
        builder.row(
            InlineKeyboardButton(
                text=KeyboardText.HOMES,
                callback_data=PageCB(
                    key=hashkey, page=Pages.SERVER, action=Actions.LIST
                ).pack(),
            ),
            width=1,
        )

        return builder.as_markup()
