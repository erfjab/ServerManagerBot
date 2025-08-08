from typing import List
from eiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from eiogram.utils.inline_builder import InlineKeyboardBuilder

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
                text=Buttons.CREATE_CREATE, callback_data=BotCB(area=AreaType.CLIENT, task=TaskType.CREATE).pack()
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
            callback_data=BotCB(area=AreaType.SERVER, task=TaskType.LIST, target=id).pack(),
        )
        kb.add(
            text=Buttons.SNAPSHOTS,
            callback_data=BotCB(area=AreaType.SNAPSHOT, task=TaskType.LIST, target=id).pack(),
        )
        kb.add(
            text=Buttons.PRIMARY_IPS,
            callback_data=BotCB(area=AreaType.PRIMARY_IP, task=TaskType.LIST, target=id).pack(),
        )
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

        kb.adjust(1, 2, 2, 1)

        cls._back(kb=kb)

        return kb.as_markup()

    @classmethod
    def clients_back(cls, id: int) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.add(
            text=Buttons.BACK,
            callback_data=BotCB(area=AreaType.CLIENT, task=TaskType.MENU, target=id).pack(),
        )
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
