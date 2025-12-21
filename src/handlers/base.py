from eiogram import Router
from eiogram.types import Message, CallbackQuery
from eiogram.filters import Command, IgnoreStateFilter
from eiogram.state import StateManager

from src.db import UserMessage, AsyncSession, Client, User
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.lang import Dialogs

router = Router()


@router.message(Command("start"), IgnoreStateFilter())
async def start_handler(message: Message, db: AsyncSession, state: StateManager, dbuser: User):
    await state.clear_all(db=db)
    clients = await Client.get_all(db)
    if not dbuser.is_owner:
        clients = [client for client in clients if client.id in dbuser.client_ids()]
    update = await message.answer(
        text=Dialogs.COMMAND_START, reply_markup=BotKB.home(clients=clients, is_owner=dbuser.is_owner)
    )
    return await UserMessage.clear(update)


@router.callback_query(BotCB.filter(area=AreaType.HOME, task=TaskType.MENU), IgnoreStateFilter())
async def home_menu(callback_query: CallbackQuery, db: AsyncSession, state: StateManager, dbuser: User):
    await state.clear_all(db=db)

    clients = await Client.get_all(db)
    if not dbuser.is_owner:
        clients = [client for client in clients if client.id in dbuser.client_ids()]
    update = await callback_query.message.answer(
        text=Dialogs.COMMAND_START,
        reply_markup=BotKB.home(clients=clients, is_owner=dbuser.is_owner),
    )
    return await UserMessage.clear(update)
