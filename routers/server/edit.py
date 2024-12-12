from aiogram import Router, F
from aiogram.types import CallbackQuery

from .data import server_data
from keys import Keyboards, Actions, PageCB, Pages, ServerUpdate
from language import MessageText
from api import HetznerManager
from config import EnvFile

router = Router(name="server_edit")


@router.callback_query(
    PageCB.filter(
        (
            F.action.in_(
                {
                    ServerUpdate.POWER_ON,
                    ServerUpdate.POWER_OFF,
                    ServerUpdate.REBOOT,
                    ServerUpdate.RESET_PASSWORD,
                    ServerUpdate.DELETE,
                    ServerUpdate.REBUILD,
                    ServerUpdate.RESET,
                }
            )
        )
        & (F.page.is_(Pages.SERVER))
    )
)
async def confirm_server_action(
    callback: CallbackQuery, callback_data: PageCB, key: str
):
    if (
        not callback_data.confirm
        and callback_data.action == ServerUpdate.REBUILD
        and callback_data.image_id is None
    ):
        server = await HetznerManager.get_server(key, callback_data.server_id)
        images = await HetznerManager.get_images(key, server.server_type.architecture)
        if not images:
            return await callback.answer(MessageText.CHECK_LOGS)

        await callback.message.edit_text(
            text=MessageText.IMAGE_LIST,
            reply_markup=Keyboards.rebuild(
                key=key, images=images, serverid=callback_data.server_id
            ),
        )
        return

    # Confirmation for actions
    if not callback_data.confirm:
        await callback.message.edit_text(
            text=MessageText.CONFIRM_ACTION.format(
                action=(callback_data.action.value).replace("_", " ")
            ),
            reply_markup=Keyboards.confirm(
                key,
                callback_data.action,
                callback_data.server_id,
                imageid=callback_data.image_id,
            ),
        )
        return

    await callback.message.edit_text(MessageText.WAIT)

    # Fetch server
    server = await HetznerManager.get_server(key, callback_data.server_id)
    if not server:
        return await callback.answer(MessageText.CHECK_LOGS)

    # Execute action based on callback_data.action
    action_result = await execute_server_action(callback_data, server, callback, key)

    if action_result is not None:
        await callback.answer(action_result)

    if callback_data.action == ServerUpdate.RESET_PASSWORD:
        return

    # Post-action handling
    if callback_data.action == ServerUpdate.DELETE:
        await update_server_list_ui(callback, key)
    else:
        await server_data(
            callback,
            PageCB(
                key=EnvFile.to_hash(key),
                page=Pages.SERVER,
                action=Actions.INFO,
                server_id=callback_data.server_id,
            ),
            key,
        )


async def execute_server_action(
    callback_data: PageCB, server, callback: CallbackQuery, key: str
):
    """Helper function to execute server actions based on the action type."""
    if callback_data.action == ServerUpdate.REBUILD:
        if not callback_data.image_id:
            return "Image ID not found"
        result = await HetznerManager.rebuild_server(
            key, server, callback_data.image_id
        )
        if not result:
            return MessageText.CHECK_LOGS
        return "Rebuilding server initiated"

    action_method = getattr(HetznerManager, callback_data.action)
    result = await action_method(key, server)

    if not result:
        return MessageText.CHECK_LOGS

    if callback_data.action == ServerUpdate.RESET_PASSWORD:
        new_password = result
        return await server_data(
            callback,
            PageCB(
                key=EnvFile.to_hash(key),
                page=Pages.SERVER,
                action=Actions.INFO,
                server_id=callback_data.server_id,
            ),
            key,
            new_password,
        )

    return f"{callback_data.action.capitalize()} action initiated"


async def update_server_list_ui(callback: CallbackQuery, key: str):
    """Helper function to update the server list after an action like delete."""
    await callback.message.edit_text(
        MessageText.START, reply_markup=Keyboards.menu(key)
    )
