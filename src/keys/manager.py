from typing import List
from eiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from eiogram.utils.inline_builder import InlineKeyboardBuilder
from hcloud.servers import Server
from hcloud.images import Image
from hcloud.datacenters import Datacenter
from hcloud.server_types import ServerType
from hcloud.primary_ips import PrimaryIP

from src.db import Client
from src.lang import Buttons
from .callback import BotCB, AreaType, TaskType, StepType


class BotKB:
    @classmethod
    def _back(cls, *, kb: InlineKeyboardBuilder, area: AreaType = AreaType.HOME, target: str | int = 0) -> InlineKeyboardMarkup:
        return kb.row(
            InlineKeyboardButton(
                text=Buttons.BACK,
                callback_data=BotCB(
                    area=area,
                    task=TaskType.INFO if target != 0 else TaskType.MENU,
                    target=target,
                ).pack(),
            ),
            size=1,
        )

    @classmethod
    def home(cls, *, clients: List[Client]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for client in clients:
            kb.add(
                text=client.kb_remark,
                callback_data=BotCB(area=AreaType.CLIENT, task=TaskType.MENU, target=client.id).pack(),
            )
        kb.adjust(2)
        kb.row(
            InlineKeyboardButton(
                text=Buttons.CLIENTS_CREATE, callback_data=BotCB(area=AreaType.CLIENT, task=TaskType.CREATE).pack()
            ),
            size=1,
        )
        kb.row(InlineKeyboardButton(text=Buttons.OWNER, url="https://t.me/erfjabs"), size=1)
        return kb.as_markup()

    @classmethod
    def clients_menu(cls, id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()

        kb.add(
            text=Buttons.SERVERS,
            callback_data=BotCB(area=AreaType.SERVER, task=TaskType.MENU, target=id).pack(),
        )
        kb.add(
            text=Buttons.SNAPSHOTS,
            callback_data=BotCB(area=AreaType.SNAPSHOT, task=TaskType.MENU, target=id).pack(),
        )
        kb.add(
            text=Buttons.PRIMARY_IPS,
            callback_data=BotCB(area=AreaType.PRIMARY_IP, task=TaskType.MENU, target=id).pack(),
        )
        kb.add(
            text=Buttons.CLIENTS_SETTING,
            callback_data=BotCB(area=AreaType.CLIENT, task=TaskType.INFO, target=id).pack(),
        )
        kb.adjust(1, 2, 1)

        cls._back(kb=kb)

        return kb.as_markup()

    @classmethod
    def clients_back(cls, id: int = 0) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=Buttons.BACK,
            callback_data=BotCB(area=AreaType.CLIENT, task=TaskType.MENU, target=id).pack(),
        )
        return kb.as_markup()

    @classmethod
    def clients_update(cls, id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=Buttons.CLIENTS_CHANGE_REMARK,
            callback_data=BotCB(
                area=AreaType.CLIENT,
                task=TaskType.UPDATE,
                target=id,
                step=StepType.CHANGE_REMARK,
            ).pack(),
        )
        kb.add(
            text=Buttons.CLIENTS_CHANGE_SECRET,
            callback_data=BotCB(
                area=AreaType.CLIENT,
                task=TaskType.UPDATE,
                target=id,
                step=StepType.CHANGE_SECRET,
            ).pack(),
        )
        kb.add(
            text=Buttons.CLIENTS_REMOVE,
            callback_data=BotCB(
                area=AreaType.CLIENT,
                task=TaskType.UPDATE,
                target=id,
                step=StepType.REMOVE_CLIENT,
            ).pack(),
        )
        kb.adjust(1)
        cls._back(kb=kb)
        return kb.as_markup()

    @classmethod
    def home_back(cls) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=Buttons.BACK,
            callback_data=BotCB(area=AreaType.HOME, task=TaskType.MENU).pack(),
        )
        return kb.as_markup()

    @classmethod
    def approval(cls, area: AreaType, task: TaskType) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=Buttons.YES,
            callback_data=BotCB(area=area, task=task, is_approve=True).pack(),
        )
        kb.add(
            text=Buttons.NO,
            callback_data=BotCB(area=area, task=task, is_approve=False).pack(),
        )
        cls._back(kb=kb, area=area)
        return kb.as_markup()

    @classmethod
    def servers_menu(cls, servers: List[Server]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        emoji = {"starting": "🟡", "stopping": "🔴", "running": "🟢", "off": "🔴"}
        for server in servers:
            kb.add(
                text=f"{emoji.get(server.status, '⚪️')} {server.name} [{server.status}]",
                callback_data=BotCB(area=AreaType.SERVER, task=TaskType.INFO, target=server.id).pack(),
            )
        kb.adjust(2)
        kb.row(
            InlineKeyboardButton(
                text=Buttons.SERVERS_CREATE,
                callback_data=BotCB(area=AreaType.SERVER, task=TaskType.CREATE).pack(),
            ),
            InlineKeyboardButton(
                text=Buttons.BACK,
                callback_data=BotCB(area=AreaType.HOME, task=TaskType.MENU).pack(),
            ),
            size=2,
        )
        return kb.as_markup()

    @classmethod
    def servers_update(cls, server: Server) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        update = {
            StepType.SERVERS_REMARK: Buttons.SERVERS_REMARK,
            StepType.SERVERS_UPGRADE: Buttons.SERVERS_UPGRADE,
            StepType.SERVERS_POWER_OFF: Buttons.SERVERS_POWER_OFF,
            StepType.SERVERS_POWER_ON: Buttons.SERVERS_POWER_ON,
            StepType.SERVERS_CREATE_SNAPSHOT: Buttons.SERVERS_CREATE_SNAPSHOT,
            StepType.SERVERS_REBOOT: Buttons.SERVERS_REBOOT,
            StepType.SERVERS_REBUILD: Buttons.SERVERS_REBUILD,
            StepType.SERVERS_DEL_SNAPSHOT: Buttons.SERVERS_DEL_SNAPSHOT,
            StepType.SERVERS_RESET_PASSWORD: Buttons.SERVERS_RESET_PASSWORD,
            StepType.SERVERS_RESET: Buttons.SERVERS_RESET,
            StepType.SERVERS_REMOVE: Buttons.SERVERS_REMOVE,
            StepType.SERVERS_UNASSIGN_IPV4: Buttons.SERVERS_UNASSIGN_IPV4,
            StepType.SERVERS_UNASSIGN_IPV6: Buttons.SERVERS_UNASSIGN_IPV6,
            StepType.SERVERS_ASSIGN_IPV4: Buttons.SERVERS_ASSIGN_IPV4,
            StepType.SERVERS_ASSIGN_IPV6: Buttons.SERVERS_ASSIGN_IPV6,
        }
        for step, button in update.items():
            kb.add(
                text=button,
                callback_data=BotCB(
                    area=AreaType.SERVER,
                    task=TaskType.UPDATE,
                    target=server.id,
                    step=step,
                ).pack(),
            )
        kb.adjust(1, 1, 2, 1, 2, 1, 2, 1, 2, 2)
        cls._back(kb=kb, area=AreaType.SERVER)
        return kb.as_markup()

    @classmethod
    def servers_back(cls, id: int = 0) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        cls._back(kb=kb, area=AreaType.SERVER, target=id)
        return kb.as_markup()

    @classmethod
    def images_select(cls, images: List[Image], task: TaskType, target: int = 0) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for image in images:
            kb.add(
                text=image.name or image.description,
                callback_data=BotCB(
                    area=AreaType.SERVER,
                    task=task,
                    target=image.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.SERVER, target=target)
        return kb.as_markup()

    @classmethod
    def datacenters_select(cls, datacenters: List[Datacenter]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for datacenter in datacenters:
            kb.add(
                text=f"{datacenter.location.city} [{datacenter.location.country}]",
                callback_data=BotCB(
                    area=AreaType.SERVER,
                    task=TaskType.CREATE,
                    target=datacenter.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.SERVER)
        return kb.as_markup()

    @classmethod
    def plans_select(cls, plans: List[ServerType]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for plan in plans:
            kb.add(
                text=f"{plan.name} [{plan.memory} RAM, {plan.cores} CPU, {float(plan.prices[0]['price_monthly']['net'])} EUR]",
                callback_data=BotCB(
                    area=AreaType.SERVER,
                    task=TaskType.CREATE,
                    target=plan.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.SERVER)
        return kb.as_markup()

    @classmethod
    def upgrade_plans_select(cls, plans: List[ServerType], server_id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for plan in plans:
            kb.add(
                text=f"{plan.name} [{plan.memory} RAM, {plan.cores} CPU, {float(plan.prices[0]['price_monthly']['net'])} EUR]",
                callback_data=BotCB(
                    area=AreaType.SERVER,
                    task=TaskType.UPDATE,
                    target=plan.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.SERVER, target=server_id)
        return kb.as_markup()

    @classmethod
    def snapshots_menu(cls, snapshots: List[Image]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for snapshot in snapshots:
            kb.add(
                text=snapshot.name or snapshot.description,
                callback_data=BotCB(
                    area=AreaType.SNAPSHOT,
                    task=TaskType.INFO,
                    target=snapshot.id,
                ).pack(),
            )
        kb.adjust(1)
        kb.row(
            InlineKeyboardButton(
                text=Buttons.SNAPSHOTS_CREATE,
                callback_data=BotCB(area=AreaType.SNAPSHOT, task=TaskType.CREATE).pack(),
            ),
            InlineKeyboardButton(
                text=Buttons.BACK,
                callback_data=BotCB(area=AreaType.HOME, task=TaskType.MENU).pack(),
            ),
            size=2,
        )
        return kb.as_markup()

    @classmethod
    def snapshots_update(cls, snapshot: Image) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        updates = {
            Buttons.SNAPSHOTS_REMARK: StepType.SNAPSHOTS_REMARK,
            Buttons.SNAPSHOTS_DELETE: StepType.SNAPSHOTS_DELETE,
        }
        for button, step in updates.items():
            kb.add(
                text=button,
                callback_data=BotCB(
                    area=AreaType.SNAPSHOT,
                    task=TaskType.UPDATE,
                    step=step,
                    target=snapshot.id,
                ).pack(),
            )
        kb.adjust(2)
        cls._back(kb=kb, area=AreaType.SNAPSHOT)
        return kb.as_markup()

    @classmethod
    def snapshots_back(cls, id: int = 0) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        cls._back(kb=kb, area=AreaType.SNAPSHOT, target=id)
        return kb.as_markup()

    @classmethod
    def snapshots_select_server(
        cls, servers: List[Server], task: TaskType = TaskType.CREATE, target: int = 0
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for server in servers:
            kb.add(
                text=server.name,
                callback_data=BotCB(
                    area=AreaType.SNAPSHOT,
                    task=task,
                    target=server.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.SNAPSHOT, target=target)
        return kb.as_markup()

    @classmethod
    def primary_ips_menu(cls, primary_ips: List[PrimaryIP]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for primary_ip in primary_ips:
            kb.add(
                text=f"{primary_ip.name} [{primary_ip.ip}]",
                callback_data=BotCB(
                    area=AreaType.PRIMARY_IP,
                    task=TaskType.INFO,
                    target=primary_ip.id,
                ).pack(),
            )
        kb.adjust(1)
        kb.row(
            InlineKeyboardButton(
                text=Buttons.PRIMARY_IPS_CREATE_IPV4,
                callback_data=BotCB(area=AreaType.PRIMARY_IP, task=TaskType.CREATE, target="ipv4").pack(),
            ),
            InlineKeyboardButton(
                text=Buttons.PRIMARY_IPS_CREATE_IPV6,
                callback_data=BotCB(area=AreaType.PRIMARY_IP, task=TaskType.CREATE, target="ipv6").pack(),
            ),
            size=2,
        )
        cls._back(kb=kb)
        return kb.as_markup()

    @classmethod
    def primary_ips_update(cls, primary_ip: PrimaryIP) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        updates = {
            Buttons.PRIMARY_IPS_REMARK: StepType.PRIMARY_IPS_REMARK,
            Buttons.PRIMARY_IPS_UNASSIGN: StepType.PRIMARY_IPS_UNASSIGN,
            Buttons.PRIMARY_IPS_ASSIGN: StepType.PRIMARY_IPS_ASSIGN,
            Buttons.PRIMARY_IPS_DELETE: StepType.PRIMARY_IPS_DELETE,
        }
        for button, step in updates.items():
            kb.add(
                text=button,
                callback_data=BotCB(
                    area=AreaType.PRIMARY_IP,
                    task=TaskType.UPDATE,
                    step=step,
                    target=primary_ip.id,
                ).pack(),
            )
        kb.adjust(1, 2, 1)
        cls._back(kb=kb, area=AreaType.PRIMARY_IP)
        return kb.as_markup()

    @classmethod
    def primary_ips_back(cls, id: int = 0) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        cls._back(kb=kb, area=AreaType.PRIMARY_IP, target=id)
        return kb.as_markup()

    @classmethod
    def primary_ips_select_server(
        cls, servers: List[Server], task: TaskType = TaskType.UPDATE, target: int = 0
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for server in servers:
            kb.add(
                text=server.name,
                callback_data=BotCB(
                    area=AreaType.PRIMARY_IP,
                    task=task,
                    target=server.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.PRIMARY_IP, target=target)
        return kb.as_markup()

    @classmethod
    def primary_ips_select_datacenter(
        cls, datacenters: List[Datacenter], task: TaskType = TaskType.CREATE, target: int = 0
    ) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for datacenter in datacenters:
            kb.add(
                text=f"{datacenter.location.city} [{datacenter.location.country}]",
                callback_data=BotCB(
                    area=AreaType.PRIMARY_IP,
                    task=task,
                    target=datacenter.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.PRIMARY_IP, target=target)
        return kb.as_markup()

    @classmethod
    def servers_primary_ips_select(cls, primary_ips: List[PrimaryIP]) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for primary_ip in primary_ips:
            kb.add(
                text=f"{primary_ip.name} [{primary_ip.ip}]",
                callback_data=BotCB(
                    area=AreaType.SERVER,
                    task=TaskType.UPDATE,
                    target=primary_ip.id,
                ).pack(),
            )
        kb.adjust(1)
        cls._back(kb=kb, area=AreaType.SERVER)
        return kb.as_markup()
