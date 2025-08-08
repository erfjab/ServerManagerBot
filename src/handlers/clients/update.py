from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.filters import Text, StateFilter
from eiogram.state import StateManager, State, StateGroup

from src.db import AsyncSession, Client, UserMessage
from src.keys import BotKB, BotCB, AreaType, TaskType, StepType
from src.lang import Dialogs

router = Router()


class ClientUpdateForm(StateGroup):
    input = State()
    approval = State()


@router.callback_query(BotCB.filter(area=AreaType.CLIENT, task=TaskType.UPDATE))
async def clients_update(
    callback_query: CallbackQuery, callback_data: BotCB, db: AsyncSession, state: StateManager, state_data: dict
):
    kb = BotKB.clients_back(id=state_data["client_id"])
    match callback_data.step:
        case StepType.CHANGE_REMARK:
            text = Dialogs.CLIENTS_ENTER_REMARK
            _state = ClientUpdateForm.input
        case StepType.CHANGE_SECRET:
            text = Dialogs.CLIENTS_ENTER_SECRET
            _state = ClientUpdateForm.input
        case StepType.REMOVE_CLIENT:
            text = Dialogs.ACTIONS_CONFIRM
            kb = BotKB.approval(area=AreaType.CLIENT, task=TaskType.UPDATE)
            _state = ClientUpdateForm.approval
        case _:
            return await callback_query.answer(text="Invalid step!", show_alert=True)
    await state.upsert_context(db=db, state=_state, step=callback_data.step)
    return await callback_query.message.edit(text=text, reply_markup=kb)


@router.message(StateFilter(ClientUpdateForm.input), Text())
async def input_handler(message: Message, db: AsyncSession, state: StateManager, state_data: dict):
    client = await Client.get_by_id(db, state_data["client_id"])
    if not client:
        update = await message.answer(text=Dialogs.CLIENTS_NOT_FOUND, reply_markup=BotKB.home_back())
        return await UserMessage.clear(update)

    match state_data["step"]:
        case StepType.CHANGE_REMARK:
            await Client.update(db, client.id, remark=message.text)
        case StepType.CHANGE_SECRET:
            await Client.update(db, client.id, secret=message.text)
        case _:
            update = await message.answer(text="Invalid step!", reply_markup=BotKB.home_back())
            return await UserMessage.clear(update)

    await state.clear_state(db=db)
    update = await message.answer(text=Dialogs.ACTIONS_SUCCESS, reply_markup=BotKB.clients_back(id=client.id))
    return await UserMessage.clear(update)


@router.callback_query(StateFilter(ClientUpdateForm.approval), BotCB.filter(area=AreaType.CLIENT, task=TaskType.UPDATE))
async def approval_handler(
    callback_query: CallbackQuery, callback_data: BotCB, db: AsyncSession, state: StateManager, state_data: dict
):
    client = await Client.get_by_id(db, state_data["client_id"])
    if not client:
        return await callback_query.answer(text=Dialogs.CLIENTS_NOT_FOUND, show_alert=True)

    if not callback_data.is_approve:
        return await callback_query.message.edit(text=Dialogs.ACTIONS_CANCELLED, reply_markup=BotKB.home_back())

    match state_data["step"]:
        case StepType.REMOVE_CLIENT:
            await Client.remove(db, client.id)

    await state.clear_state(db=db)
    return await callback_query.message.edit(text=Dialogs.ACTIONS_SUCCESS, reply_markup=BotKB.home_back())
