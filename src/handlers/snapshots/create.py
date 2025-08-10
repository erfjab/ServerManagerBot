from eiogram import Router
from eiogram.types import CallbackQuery, Message
from eiogram.filters import Text, StateFilter
from eiogram.state import StateManager, State, StateGroup

from src.db import AsyncSession, UserMessage
from src.keys import BotKB, BotCB, AreaType, TaskType
from src.lang import Dialogs
from src.utils.depends import GetHetzner

router = Router()


class SnapshotCreateForm(StateGroup):
    remark = State()
    server = State()


@router.callback_query(BotCB.filter(area=AreaType.SNAPSHOT, task=TaskType.CREATE))
async def snapshots_create(callback_query: CallbackQuery, db: AsyncSession, state: StateManager, hetzner: GetHetzner):
    servers = hetzner.servers.get_all()
    if not servers:
        return await callback_query.answer(text=Dialogs.SNAPSHOTS_SERVERS_NOT_FOUND, show_alert=True)
    await state.upsert_context(db=db, state=SnapshotCreateForm.remark)
    return await callback_query.message.edit(text=Dialogs.SNAPSHOTS_ENTER_REMARK, reply_markup=BotKB.snapshots_back())


@router.message(StateFilter(SnapshotCreateForm.remark), Text())
async def remark_handler(message: Message, db: AsyncSession, state: StateManager, hetzner: GetHetzner):
    servers = hetzner.servers.get_all()
    if not servers:
        update = await message.answer(text=Dialogs.SNAPSHOTS_SERVERS_NOT_FOUND)
        return await UserMessage.clear(update)

    await state.upsert_context(db=db, state=SnapshotCreateForm.server, remark=message.text)
    update = await message.answer(
        text=Dialogs.SNAPSHOTS_SELECT_SERVER, reply_markup=BotKB.snapshots_select_server(servers=servers)
    )
    return await UserMessage.clear(update)


@router.callback_query(StateFilter(SnapshotCreateForm.server), BotCB.filter(area=AreaType.SNAPSHOT, task=TaskType.CREATE))
async def server_handler(
    callback_query: CallbackQuery,
    callback_data: BotCB,
    db: AsyncSession,
    state: StateManager,
    hetzner: GetHetzner,
    state_data: dict,
):
    server = hetzner.servers.get_by_id(int(callback_data.target))
    if not server:
        return await callback_query.answer(text=Dialogs.SNAPSHOTS_SERVER_NOT_FOUND, show_alert=True)

    try:
        snapshot = server.create_image(description=state_data["remark"], type="snapshot")
    except Exception:
        return await callback_query.answer(text=Dialogs.ACTIONS_FAILED, show_alert=True)

    await state.clear_state(db=db)
    return await callback_query.message.edit(
        text=Dialogs.SNAPSHOTS_CREATE_SUCCESS, reply_markup=BotKB.snapshots_back(snapshot.image.id)
    )
