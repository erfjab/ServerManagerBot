from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.filters import StateFilter, Text
from eiogram.state import StateManager, State, StateGroup

from src.db import AsyncSession
from src.keys import BotKB, BotCB, AreaType, TaskType, StepType
from src.lang import Dialogs
from src.utils.depends import GetHetzner

router = Router()


class SnapshotUpdateForm(StateGroup):
    approval = State()
    input = State()
    select = State()


@router.callback_query(BotCB.filter(area=AreaType.SNAPSHOT, task=TaskType.UPDATE))
async def snapshots_update(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
):
    kb = BotKB.snapshots_back(id=callback_data.target)
    snapshot = hetzner.images.get_by_id(int(callback_data.target))
    if not snapshot:
        return await callback_query.message.edit(text=Dialogs.SNAPSHOTS_NOT_FOUND, reply_markup=kb)
    match callback_data.step:
        case StepType.SNAPSHOTS_DELETE:
            text = Dialogs.ACTIONS_CONFIRM
            _state = SnapshotUpdateForm.approval
            kb = BotKB.approval(area=AreaType.SNAPSHOT, task=TaskType.UPDATE)
        case StepType.SNAPSHOTS_REMARK:
            text = Dialogs.SNAPSHOTS_ENTER_REMARK
            _state = SnapshotUpdateForm.input
        case _:
            return await callback_query.answer(text="Invalid step!", show_alert=True)
    await state.upsert_context(db=db, state=_state, step=callback_data.step, target=callback_data.target)
    return await callback_query.message.edit(text=text, reply_markup=kb)


@router.message(StateFilter(SnapshotUpdateForm.input), Text())
async def input_handler(
    message: Message,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    snapshot = hetzner.images.get_by_id(int(state_data["target"]))
    if not snapshot:
        return await message.answer(text=Dialogs.SNAPSHOTS_NOT_FOUND)

    match state_data["step"]:
        case StepType.SNAPSHOTS_REMARK:
            snapshot.update(description=message.text)
        case _:
            return await message.answer(text="Invalid step!", reply_markup=BotKB.snapshots_back(id=snapshot.id))

    await state.clear_state(db=db)
    return await message.answer(text=Dialogs.SNAPSHOTS_UPDATE_SUCCESS, reply_markup=BotKB.snapshots_back(id=snapshot.id))


@router.callback_query(StateFilter(SnapshotUpdateForm.approval), BotCB.filter(area=AreaType.SNAPSHOT, task=TaskType.UPDATE))
async def approval_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    if not callback_data.is_approve:
        return await callback_query.message.edit(text=Dialogs.ACTIONS_CANCELLED, reply_markup=BotKB.snapshots_back())

    snapshot = hetzner.images.get_by_id(int(state_data["target"]))
    if not snapshot:
        return await callback_query.answer(text=Dialogs.SNAPSHOTS_NOT_FOUND, show_alert=True)

    kb = BotKB.snapshots_back(id=snapshot.id)
    match state_data["step"]:
        case StepType.SNAPSHOTS_DELETE:
            snapshot.delete()
            kb = BotKB.snapshots_back()

    await state.clear_state(db=db)
    return await callback_query.message.edit(text=Dialogs.SNAPSHOTS_UPDATE_SUCCESS, reply_markup=kb)
