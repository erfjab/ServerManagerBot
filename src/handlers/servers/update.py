import asyncio
from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.filters import StateFilter, Text
from eiogram.state import StateManager, State, StateGroup

from src.db import AsyncSession, UserMessage
from src.keys import BotKB, BotCB, AreaType, TaskType, StepType
from src.lang import Dialogs
from src.utils.depends import GetHetzner

router = Router()


class ServerUpdateForm(StateGroup):
    approval = State()
    image = State()
    ip = State()
    input = State()


@router.callback_query(BotCB.filter(area=AreaType.SERVER, task=TaskType.UPDATE))
async def servers_update(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
):
    kb = BotKB.servers_back(id=callback_data.target)
    server = hetzner.servers.get_by_id(int(callback_data.target))
    if not server:
        return await callback_query.message.edit(text=Dialogs.SERVERS_NOT_FOUND, reply_markup=kb)
    match callback_data.step:
        case (
            StepType.SERVERS_POWER_OFF
            | StepType.SERVERS_POWER_ON
            | StepType.SERVERS_RESET_PASSWORD
            | StepType.SERVERS_RESET
            | StepType.SERVERS_REBOOT
            | StepType.SERVERS_REMOVE
            | StepType.SERVERS_CREATE_SNAPSHOT
            | StepType.SERVERS_UNASSIGN_IPV4
            | StepType.SERVERS_UNASSIGN_IPV6
        ):
            text = Dialogs.ACTIONS_CONFIRM
            _state = ServerUpdateForm.approval
            kb = BotKB.approval(area=AreaType.SERVER, task=TaskType.UPDATE)
        case StepType.SERVERS_ASSIGN_IPV4 | StepType.SERVERS_ASSIGN_IPV6:
            ip_type = "ipv4" if callback_data.step == StepType.SERVERS_ASSIGN_IPV4 else "ipv6"
            if ip_type == "ipv4" and server.public_net.primary_ipv4:
                return await callback_query.answer(text=Dialogs.SERVERS_ASSIGN_UNASSIGN_IPV4, show_alert=True)
            if ip_type == "ipv6" and server.public_net.primary_ipv6:
                return await callback_query.answer(text=Dialogs.SERVERS_ASSIGN_UNASSIGN_IPV6, show_alert=True)
            primary_ips = hetzner.primary_ips.get_all()
            if not primary_ips:
                return await callback_query.answer(text=Dialogs.SERVERS_PRIMARY_IPS_NOT_FOUND, show_alert=True)
            filtered_ips = [ip for ip in primary_ips if not ip.assignee_id and ip.type == ip_type]
            if not filtered_ips:
                return await callback_query.answer(text=Dialogs.SERVERS_PRIMARY_IPS_NOT_FOUND, show_alert=True)
            text = Dialogs.SERVERS_ASSIGN_SELECT
            _state = ServerUpdateForm.ip
            kb = BotKB.servers_primary_ips_select(primary_ips=filtered_ips)
        case StepType.SERVERS_REBUILD:
            text = Dialogs.SERVERS_REBUILD_CONFIRM
            _state = ServerUpdateForm.image
            images = hetzner.images.get_all(type=["system", "snapshot"], architecture=server.image.architecture)
            if not images:
                return await callback_query.answer(text=Dialogs.SERVERS_IMAGES_NOT_FOUND, show_alert=True)
            images.sort(key=lambda x: x.name or x.description)
            images.sort(key=lambda x: x.type, reverse=True)
            kb = BotKB.images_select(images=images, task=TaskType.UPDATE, target=callback_data.target)
        case StepType.SERVERS_DEL_SNAPSHOT:
            text = Dialogs.SERVERS_SNAPSHOT_DELETE_CONFIRM
            _state = ServerUpdateForm.image
            images = hetzner.images.get_all(type="snapshot")
            if not images:
                return await callback_query.answer(text=Dialogs.SERVERS_SNAPSHOT_NOT_FOUND, show_alert=True)
            images = [img for img in images if img.created_from and img.created_from.id == int(callback_data.target)]
            if not images:
                return await callback_query.answer(text=Dialogs.SERVERS_SNAPSHOT_NOT_FOUND, show_alert=True)
            kb = BotKB.images_select(images=images, task=TaskType.UPDATE, target=int(callback_data.target))
        case StepType.SERVERS_REMARK:
            text = Dialogs.SERVERS_ENTER_REMARK
            _state = ServerUpdateForm.input
        case _:
            return await callback_query.answer(text="Invalid step!", show_alert=True)
    await state.upsert_context(db=db, state=_state, step=callback_data.step, target=callback_data.target)
    return await callback_query.message.edit(text=text, reply_markup=kb)


@router.callback_query(StateFilter(ServerUpdateForm.image), BotCB.filter(area=AreaType.SERVER, task=TaskType.UPDATE))
async def select_image_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
):
    await state.upsert_context(db=db, state=ServerUpdateForm.approval, image_id=callback_data.target)
    return await callback_query.message.edit(
        text=Dialogs.ACTIONS_CONFIRM,
        reply_markup=BotKB.approval(area=AreaType.SERVER, task=TaskType.UPDATE),
    )


@router.message(StateFilter(ServerUpdateForm.input), Text())
async def input_handler(message: Message, state: StateManager, db: StateFilter, state_data: dict, hetzner: GetHetzner):
    server = hetzner.servers.get_by_id(int(state_data["target"]))
    if not server:
        update = await message.answer(text=Dialogs.SERVERS_NOT_FOUND, reply_markup=BotKB.servers_back())
        return await UserMessage.add(update)

    match state_data["step"]:
        case StepType.SERVERS_REMARK:
            if len(message.text.split(" ")) > 1:
                update = await message.answer(text=Dialogs.SERVERS_REMARK_VALIDATION)
                return await UserMessage.add(update)
            server.update(name=message.text)

    await state.clear_state(db=db)
    update = await message.answer(text=Dialogs.ACTIONS_SUCCESS, reply_markup=BotKB.servers_back(server.id))
    return await UserMessage.clear(update)


@router.callback_query(StateFilter(ServerUpdateForm.ip), BotCB.filter(area=AreaType.SERVER, task=TaskType.UPDATE))
async def select_ip_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    primary_ip = hetzner.primary_ips.get_by_id(int(callback_data.target))
    if not primary_ip:
        return await callback_query.message.edit(text=Dialogs.SERVERS_PRIMARY_IPS_NOT_FOUND, reply_markup=BotKB.home_back())
    server = hetzner.servers.get_by_id(int(state_data["target"]))
    if not server:
        return await callback_query.answer(text=Dialogs.SERVERS_NOT_FOUND, show_alert=True)

    await callback_query.message.edit(text=Dialogs.ACTIONS_WAITING)
    if server.status != "off":
        server.power_off()
    await asyncio.sleep(2)
    primary_ip.assign(assignee_id=server.id, assignee_type="server")
    await asyncio.sleep(2)
    await state.clear_state(db=db)
    return await callback_query.message.edit(text=Dialogs.ACTIONS_SUCCESS, reply_markup=BotKB.servers_back(server.id))


@router.callback_query(StateFilter(ServerUpdateForm.approval), BotCB.filter(area=AreaType.SERVER, task=TaskType.UPDATE))
async def approval_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    state_data: dict,
    hetzner: GetHetzner,
):
    if not callback_data.is_approve:
        return await callback_query.message.edit(text=Dialogs.ACTIONS_CANCELLED, reply_markup=BotKB.servers_back())

    server = hetzner.servers.get_by_id(int(state_data["target"]))
    if not server:
        return await callback_query.message.edit(text=Dialogs.SERVERS_NOT_FOUND, reply_markup=BotKB.home_back())

    kb = BotKB.servers_back(id=server.id)
    match state_data["step"]:
        case StepType.SERVERS_UNASSIGN_IPV4:
            await callback_query.message.edit(text=Dialogs.ACTIONS_WAITING)
            if server.status != "off":
                server.power_off()
            await asyncio.sleep(2)
            if server.public_net.primary_ipv4:
                server.public_net.primary_ipv4.unassign()
        case StepType.SERVERS_UNASSIGN_IPV6:
            await callback_query.message.edit(text=Dialogs.ACTIONS_WAITING)
            if server.status != "off":
                server.power_off()
            await asyncio.sleep(2)
            if server.public_net.primary_ipv6:
                server.public_net.primary_ipv6.unassign()
        case StepType.SERVERS_POWER_OFF:
            server.power_off()
        case StepType.SERVERS_POWER_ON:
            server.power_on()
        case StepType.SERVERS_RESET_PASSWORD:
            password = server.reset_password()
            await callback_query.message.answer(
                text=Dialogs.SERVERS_PASSWORD_RESET_SUCCESS.format(password=password.root_password),
            )
        case StepType.SERVERS_RESET:
            server.reset()
        case StepType.SERVERS_REBOOT:
            server.reboot()
        case StepType.SERVERS_CREATE_SNAPSHOT:
            server.create_image(type="snapshot")
        case StepType.SERVERS_REMOVE:
            server.delete()
            kb = BotKB.servers_back()
        case StepType.SERVERS_REBUILD:
            image = hetzner.images.get_by_id(int(state_data["image_id"]))
            if not image:
                return await callback_query.message.edit(text=Dialogs.SERVERS_IMAGES_NOT_FOUND, reply_markup=BotKB.home_back())
            server.rebuild(image=image)
        case StepType.SERVERS_DEL_SNAPSHOT:
            image = hetzner.images.get_by_id(int(state_data["image_id"]))
            if not image:
                return await callback_query.message.edit(
                    text=Dialogs.SERVERS_SNAPSHOT_NOT_FOUND, reply_markup=BotKB.home_back()
                )
            image.delete()

    await state.clear_state(db=db)
    return await callback_query.message.edit(text=Dialogs.ACTIONS_SUCCESS, reply_markup=kb)
