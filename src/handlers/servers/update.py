from eiogram import Router
from eiogram.types import CallbackQuery
from eiogram.filters import StateFilter
from eiogram.state import StateManager, State, StateGroup

from src.db import AsyncSession
from src.keys import BotKB, BotCB, AreaType, TaskType, StepType
from src.lang import Dialogs
from src.utils.depends import GetHetzner

router = Router()


class ServerUpdateForm(StateGroup):
    approval = State()
    select = State()


@router.callback_query(BotCB.filter(area=AreaType.SERVER, task=TaskType.UPDATE))
async def servers_update(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
):
    kb = BotKB.servers_back(id=callback_data.target)
    match callback_data.step:
        case (
            StepType.SERVERS_POWER_OFF
            | StepType.SERVERS_POWER_ON
            | StepType.SERVERS_RESET_PASSWORD
            | StepType.SERVERS_RESET
            | StepType.SERVERS_REBOOT
            | StepType.SERVERS_REMOVE
        ):
            text = Dialogs.ACTIONS_CONFIRM
            _state = ServerUpdateForm.approval
            kb = BotKB.approval(area=AreaType.SERVER, task=TaskType.UPDATE)
        case StepType.SERVERS_REBUILD:
            text = Dialogs.SERVERS_REBUILD_CONFIRM
            _state = ServerUpdateForm.select
            images = hetzner.images.get_all()
            if not images:
                return await callback_query.answer(text=Dialogs.SERVERS_IMAGES_NOT_FOUND, show_alert=True)
            kb = BotKB.images_select(images=images, task=TaskType.UPDATE, target=callback_data.target)
        case _:
            return await callback_query.answer(text="Invalid step!", show_alert=True)
    await state.upsert_context(db=db, state=_state, step=callback_data.step, target=callback_data.target)
    return await callback_query.message.edit(text=text, reply_markup=kb)


@router.callback_query(StateFilter(ServerUpdateForm.select), BotCB.filter(area=AreaType.SERVER, task=TaskType.UPDATE))
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
        return await callback_query.message.edit(text=Dialogs.ACTIONS_CANCELLED, reply_markup=BotKB.home_back())

    server = hetzner.servers.get_by_id(int(state_data["target"]))
    if not server:
        return await callback_query.message.edit(text=Dialogs.SERVERS_NOT_FOUND, reply_markup=BotKB.home_back())

    kb = BotKB.servers_back(id=server.id)
    match state_data["step"]:
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
        case StepType.SERVERS_REMOVE:
            server.delete()
            kb = BotKB.servers_back()
        case StepType.SERVERS_REBUILD:
            image = hetzner.images.get_by_id(int(state_data["image_id"]))
            if not image:
                return await callback_query.message.edit(text=Dialogs.SERVERS_IMAGES_NOT_FOUND, reply_markup=BotKB.home_back())
            server.rebuild(image=image)

    await state.clear_state(db=db)
    return await callback_query.message.edit(text=Dialogs.ACTIONS_SUCCESS, reply_markup=kb)
