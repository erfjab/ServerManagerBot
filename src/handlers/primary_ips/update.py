import asyncio

from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.filters import StateFilter, Text
from eiogram.state import StateManager, State, StateGroup

from src.db import AsyncSession
from src.keys import BotKB, BotCB, AreaType, TaskType, StepType
from src.lang import Dialogs
from src.utils.depends import GetHetzner

router = Router()


class PrimaryUpdateForm(StateGroup):
    approval = State()
    input = State()
    select = State()


@router.callback_query(BotCB.filter(area=AreaType.PRIMARY_IP, task=TaskType.UPDATE))
async def primary_ips_update(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
):
    kb = BotKB.primary_ips_back(id=callback_data.target)
    primary_ip = hetzner.primary_ips.get_by_id(int(callback_data.target))
    if not primary_ip:
        return await callback_query.message.edit(text=Dialogs.PRIMARY_IP_NOT_FOUND, reply_markup=kb)
    match callback_data.step:
        case StepType.PRIMARY_IPS_DELETE | StepType.PRIMARY_IPS_UNASSIGN:
            text = Dialogs.ACTIONS_CONFIRM
            _state = PrimaryUpdateForm.approval
            kb = BotKB.approval(area=AreaType.PRIMARY_IP, task=TaskType.UPDATE)
        case StepType.PRIMARY_IPS_REMARK:
            text = Dialogs.PRIMARY_IP_ENTER_REMARK
            _state = PrimaryUpdateForm.input
        case StepType.PRIMARY_IPS_ASSIGN:
            servers = hetzner.servers.get_all()
            if not servers:
                return await callback_query.answer(text=Dialogs.SERVERS_NOT_FOUND, show_alert=True)
            filtered_servers = [s for s in servers if not s.public_net.ipv4]
            if not filtered_servers:
                return await callback_query.answer(text=Dialogs.SERVERS_NOT_FOUND, show_alert=True)
            text = Dialogs.PRIMARY_IP_SELECT_ASSIGNEE
            _state = PrimaryUpdateForm.select
            kb = BotKB.primary_ips_select_server(servers=filtered_servers)
        case _:
            return await callback_query.answer(text="Invalid step!", show_alert=True)
    await state.upsert_context(db=db, state=_state, step=callback_data.step, target=callback_data.target)
    return await callback_query.message.edit(text=text, reply_markup=kb)


@router.message(StateFilter(PrimaryUpdateForm.input), Text())
async def input_handler(
    message: Message,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    primary_ip = hetzner.primary_ips.get_by_id(int(state_data["target"]))
    if not primary_ip:
        return await message.answer(text=Dialogs.PRIMARY_IP_NOT_FOUND)

    match state_data["step"]:
        case StepType.PRIMARY_IPS_REMARK:
            primary_ip.update(name=message.text)
        case _:
            return await message.answer(text="Invalid step!", reply_markup=BotKB.primary_ips_back(id=primary_ip.id))

    await state.clear_state(db=db)
    return await message.answer(text=Dialogs.PRIMARY_IPS_UPDATE_SUCCESS, reply_markup=BotKB.primary_ips_back(id=primary_ip.id))


@router.callback_query(StateFilter(PrimaryUpdateForm.approval), BotCB.filter(area=AreaType.PRIMARY_IP, task=TaskType.UPDATE))
async def approval_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    if not callback_data.is_approve:
        return await callback_query.message.edit(text=Dialogs.ACTIONS_CANCELLED, reply_markup=BotKB.primary_ips_back())

    primary_ip = hetzner.primary_ips.get_by_id(int(state_data["target"]))
    if not primary_ip:
        return await callback_query.answer(text=Dialogs.PRIMARY_IP_NOT_FOUND, show_alert=True)

    kb = BotKB.primary_ips_back(id=primary_ip.id)
    match state_data["step"]:
        case StepType.PRIMARY_IPS_DELETE:
            primary_ip.delete()
            kb = BotKB.primary_ips_back()
        case StepType.PRIMARY_IPS_UNASSIGN:
            await callback_query.message.edit(text=Dialogs.ACTIONS_WAITING)
            if not primary_ip.assignee_id:
                return await callback_query.answer(text=Dialogs.PRIMARY_IP_ASSIGNEE_NOT_FOUND, show_alert=True)
            server = hetzner.servers.get_by_id(int(primary_ip.assignee_id))
            if not server:
                return await callback_query.answer(text=Dialogs.SERVERS_NOT_FOUND, show_alert=True)
            server.power_off()
            await asyncio.sleep(2)
            primary_ip.unassign()

    await state.clear_state(db=db)
    return await callback_query.message.edit(text=Dialogs.PRIMARY_IPS_UPDATE_SUCCESS, reply_markup=kb)


@router.callback_query(StateFilter(PrimaryUpdateForm.select), BotCB.filter(area=AreaType.PRIMARY_IP, task=TaskType.UPDATE))
async def select_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    primary_ip = hetzner.primary_ips.get_by_id(int(state_data["target"]))
    if not primary_ip:
        return await callback_query.answer(text=Dialogs.PRIMARY_IP_NOT_FOUND, show_alert=True)

    server = hetzner.servers.get_by_id(int(callback_data.target))
    if not server:
        return await callback_query.answer(text=Dialogs.SERVERS_NOT_FOUND, show_alert=True)

    primary_ip.assign(assignee_id=server.id, assignee_type="server")
    await asyncio.sleep(2)
    server.power_on()

    await state.clear_state(db=db)
    return await callback_query.message.edit(
        text=Dialogs.PRIMARY_IPS_UPDATE_SUCCESS, reply_markup=BotKB.primary_ips_back(id=primary_ip.id)
    )
