from eiogram import Router
from eiogram.types import Message, CallbackQuery
from eiogram.filters import Command, IgnoreStateFilter
from eiogram.state import StateManager

from src.db import UserMessage, AsyncSession, Client
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.lang import Dialogs

router = Router()


@router.message(Command("start"), IgnoreStateFilter())
async def start_handler(message: Message, db: AsyncSession, state: StateManager):
    await state.clear_all(db=db)
    clients = await Client.get_all(db)
    update = await message.answer(text=Dialogs.COMMAND_START, reply_markup=BotKB.home(clients=clients))
    return await UserMessage.clear(update)


@router.callback_query(BotCB.filter(area=AreaType.HOME, task=TaskType.MENU), IgnoreStateFilter())
async def home_menu(callback_query: CallbackQuery, db: AsyncSession, state: StateManager):
    await state.clear_all(db=db)
    clients = await Client.get_all(db)
    update = await callback_query.message.answer(
        text=Dialogs.COMMAND_START,
        reply_markup=BotKB.home(clients=clients),
    )
    return await UserMessage.clear(update)
