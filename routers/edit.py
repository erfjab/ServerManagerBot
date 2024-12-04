from aiogram import Router, F
from aiogram.types import CallbackQuery

from hcloud.servers.client import BoundServer

from .data import server_data
from keys import ServerAction, Keyboards, Actions
from language import MessageText
from api import HetznerAPI

router = Router(name="edit")


@router.callback_query(
    ServerAction.filter(
        F.action.in_(
            {
                Actions.POWER_ON,
                Actions.POWER_OFF,
                Actions.REBOOT,
                Actions.RESET_PASSWORD,
                Actions.DELETE,
                Actions.REBUILD,
                Actions.RESET,
            }
        )
    )
)
async def confirm_server_action(callback: CallbackQuery, callback_data: ServerAction):
    if (
        not callback_data.confirm
        and callback_data.action == Actions.REBUILD
        and callback_data.image_id == 0
    ):
        images = await HetznerAPI.get_images(callback.from_user.id)
        if not images:
            return await callback.answer(MessageText.CHECK_LOGS)

        await callback.message.edit_text(
            text=MessageText.IMAGE_LIST,
            reply_markup=Keyboards.rebuild(
                images=images, server_id=callback_data.server_id
            ),
        )
        return

    # Confirmation for actions
    if not callback_data.confirm:
        await callback.message.edit_text(
            text=MessageText.CONFIRM_ACTION.format(action=callback_data.action),
            reply_markup=Keyboards.confirm(
                callback_data.action,
                callback_data.server_id,
                image_id=callback_data.image_id,
            ),
        )
        return

    await callback.message.edit_text(MessageText.WAIT)

    # Fetch server
    server = await HetznerAPI.get_server(callback_data.server_id)
    if not server:
        return await callback.answer(MessageText.CHECK_LOGS)

    # Execute action based on callback_data.action
    action_result = await execute_server_action(callback_data, server, callback)

    if action_result is not None:
        await callback.answer(action_result)

    if callback_data.action == Actions.RESET_PASSWORD:
        return

    # Post-action handling
    if callback_data.action == Actions.DELETE:
        await update_server_list_ui(callback)
    else:
        await server_data(
            callback,
            ServerAction(action=Actions.INFO, server_id=callback_data.server_id),
        )


async def execute_server_action(
    callback_data: ServerAction, server: BoundServer, callback: CallbackQuery
):
    """Helper function to execute server actions based on the action type."""
    if callback_data.action == Actions.REBUILD:
        if not callback_data.image_id:
            return "Image ID not found"
        result = await HetznerAPI.rebuild_server(
            server, callback_data.image_id, callback.from_user.id
        )
        if not result:
            return MessageText.CHECK_LOGS
        return "Rebuilding server initiated"

    action_method = getattr(HetznerAPI, callback_data.action)
    result = await action_method(server, callback.from_user.id)

    if not result:
        return MessageText.CHECK_LOGS

    if callback_data.action == Actions.RESET_PASSWORD:
        new_password = result
        return await server_data(
            callback,
            ServerAction(action=Actions.INFO, server_id=callback_data.server_id),
            server_password=new_password,
        )

    return f"{callback_data.action.capitalize()} action initiated"


async def update_server_list_ui(callback: CallbackQuery):
    """Helper function to update the server list after an action like delete."""
    servers = await HetznerAPI.get_servers(callback.from_user.id)
    if not servers:
        await callback.answer(MessageText.CHECK_LOGS)
    else:
        await callback.message.edit_text(
            MessageText.START, reply_markup=Keyboards.menu(servers)
        )
