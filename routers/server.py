from aiogram import Router, F, exceptions
from aiogram.types import CallbackQuery
from models.callbacks import ServerAction, ServerList
from utils.hetzner import HetznerManager
from utils.keys import server_list_keyboard, server_action_keyboard, confirm_action_keyboard, rebuild_keyboard
from utils.lang import MessageText
from models.servers import Actions
from datetime import datetime, timezone
from hcloud.servers.client import BoundServer

router = Router()

@router.callback_query(ServerList.filter(F.action == Actions.Home))
async def update_server_list(callback: CallbackQuery, callback_data: ServerList):
    servers = await HetznerManager.get_servers(callback.from_user.id)
    if not servers:
        return await callback.answer(MessageText.CheckLogs)
    
    try:
        await callback.message.edit_text(
            MessageText.Start,
            reply_markup=server_list_keyboard(servers)
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.ServersIsUpdated)

@router.callback_query(ServerAction.filter(F.action.in_({Actions.Info, Actions.Update})))
async def server_info(callback: CallbackQuery, callback_data: ServerAction, server_password: str = None):
    server = await HetznerManager.get_server(callback_data.server_id, callback.from_user.id)

    try:
        emoji = {
            'starting': '🟡',
            'stopping': '🔴',
            'running': '🟢',
            'off' : '🔴'
        }
        server: BoundServer
        status_emoji = emoji.get(server.status, '⚪')
        await callback.message.edit_text(
            text=MessageText.ServerInfo.format(
                name=server.name,
                status=server.status,
                ip=server.public_net.ipv4.ip if server.public_net.ipv4.ip else 'No IPV4',
                ram=server.server_type.memory,
                cpu=server.server_type.cores,
                created=server.created.strftime('%Y-%m-%d'),
                country=server.datacenter.location.country,
                city=server.datacenter.location.city,
                password=server_password or '*',
                image=server.image.name,
                status_emoji=status_emoji,
                created_day=(datetime.now(tz=timezone.utc) - server.created).days,
                disk=server.server_type.disk,
            ),
            reply_markup=server_action_keyboard(server.id)
        )
    except exceptions.TelegramAPIError:
        await callback.answer(MessageText.ServerIsUpdated)


@router.callback_query(ServerAction.filter(F.action.in_({
    Actions.PowerOn, Actions.PowerOff, Actions.Reboot, Actions.ResetPassword, 
    Actions.Delete, Actions.Rebuild, Actions.Reset
})))
async def confirm_server_action(callback: CallbackQuery, callback_data: ServerAction):
    # Handling image selection for rebuilding action
    if not callback_data.confirm and callback_data.action == Actions.Rebuild and callback_data.image_id == 0:
        images = await HetznerManager.get_images(callback.from_user.id)
        if not images:
            return await callback.answer(MessageText.CheckLogs)
        
        await callback.message.edit_text(
            text=MessageText.ImagesList,
            reply_markup=rebuild_keyboard(images=images, server_id=callback_data.server_id)
        )
        return

    # Confirmation for actions
    if not callback_data.confirm:
        await callback.message.edit_text(
            text=MessageText.ConfirmAction.format(action=callback_data.action.replace('_', ' ')),
            reply_markup=confirm_action_keyboard(callback_data.action, callback_data.server_id, image_id=callback_data.image_id)
        )
        return

    await callback.message.edit_text(MessageText.Wait)

    # Fetch server
    server = await HetznerManager.get_server(callback_data.server_id, callback.from_user.id)
    if not server:
        return await callback.answer(MessageText.CheckLogs)

    # Execute action based on callback_data.action
    action_result = await execute_server_action(callback_data, server, callback)
    
    if action_result is not None:
        await callback.answer(action_result)

    if callback_data.action == Actions.ResetPassword:
        return

    # Post-action handling
    if callback_data.action == Actions.Delete:
        await update_server_list_ui(callback)
    else:
        await server_info(callback, ServerAction(action=Actions.Info, server_id=callback_data.server_id))


async def execute_server_action(callback_data: ServerAction, server: BoundServer, callback: CallbackQuery):
    """Helper function to execute server actions based on the action type."""
    if callback_data.action == Actions.Rebuild:
        if not callback_data.image_id:
            return "Image ID not found"
        result = await HetznerManager.rebuild_server(server, callback_data.image_id, callback.from_user.id)
        if not result:
            return MessageText.CheckLogs
        return "Rebuilding server initiated"

    action_method = getattr(HetznerManager, callback_data.action)
    result = await action_method(server, callback.from_user.id)
    
    if not result:
        return MessageText.CheckLogs
    
    if callback_data.action == Actions.ResetPassword:
        new_password = result
        return await server_info(callback, ServerAction(action=Actions.Info, server_id=callback_data.server_id), server_password=new_password)
        
    
    return f"{callback_data.action.capitalize()} action initiated"


async def update_server_list_ui(callback: CallbackQuery):
    """Helper function to update the server list after an action like delete."""
    servers = await HetznerManager.get_servers(callback.from_user.id)
    if not servers:
        await callback.answer(MessageText.CheckLogs)
    else:
        await callback.message.edit_text(
            MessageText.Start,
            reply_markup=server_list_keyboard(servers)
        )
