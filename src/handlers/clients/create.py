from secrets import token_hex

from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.filters import IgnoreStateFilter, Text, StateFilter
from eiogram.state import StateManager, State, StateGroup
from hcloud import Client as HCloudClient

from src.db import AsyncSession, Client, UserMessage
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.lang import Dialogs

router = Router()


class ClientCreateForm(StateGroup):
    remark = State()
    secret = State()


@router.callback_query(BotCB.filter(area=AreaType.CLIENT, task=TaskType.CREATE), IgnoreStateFilter())
async def clients_create(callback_query: CallbackQuery, db: AsyncSession, state: StateManager):
    await state.upsert_context(db=db, state=ClientCreateForm.remark)
    return await callback_query.message.edit(text=Dialogs.CLIENTS_ENTER_REMARK, reply_markup=BotKB.home_back())


@router.message(StateFilter(ClientCreateForm.remark), Text())
async def remark_handler(message: Message, db: AsyncSession, state: StateManager):
    if await Client.get_by_remark(db, message.text):
        update = await message.answer(text=Dialogs.ACTIONS_DUPLICATE, reply_markup=BotKB.home_back())
        return await UserMessage.clear(update)
    await state.upsert_context(db=db, state=ClientCreateForm.secret, remark=message.text)
    update = await message.answer(text=Dialogs.CLIENTS_ENTER_SECRET, reply_markup=BotKB.home_back())
    return await UserMessage.clear(update)


@router.message(StateFilter(ClientCreateForm.secret), Text())
async def secret_handler(message: Message, db: AsyncSession, state: StateManager, state_data: dict):
    try:
        hetzner = HCloudClient(token=message.text)
        hetzner.datacenters.get_all()
    except Exception:
        update = await message.answer(text=Dialogs.CLIENTS_INVALID_TOKEN)
        return await UserMessage.add(update)
    client = await Client.create(db, remark=state_data.get("remark", token_hex(3)), secret=message.text)
    await state.clear_all(db=db)
    update = await message.answer(text=Dialogs.CLIENTS_CREATION_SUCCESS, reply_markup=BotKB.clients_back(id=client.id))
    return await UserMessage.clear(update)
