from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from hcloud.servers.domain import Server
from models.callbacks import ServerAction, ServerList
from models.servers import Actions
from hcloud.images.domain import Image
from utils.lang import KeyboardText

def server_list_keyboard(servers: list[Server]) -> InlineKeyboardMarkup:
    keyboard = []
    
    for server in servers:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{server.name} ({server.public_net.ipv4.ip if server.public_net.ipv4 else 'No IPv4'})",
                callback_data=ServerAction(action=Actions.Info, server_id=server.id, image_id=0, confirm=False).pack()
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text=KeyboardText.Update,
            callback_data=ServerList(action=Actions.Home).pack()
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def server_action_keyboard(server_id: int) -> InlineKeyboardMarkup:
    keyboard = []
    
    actions = {
        Actions.PowerOn       : KeyboardText.PowerOn,
        Actions.PowerOff      : KeyboardText.PowerOff,
        Actions.Reboot        : KeyboardText.Reboot,
        Actions.ResetPassword : KeyboardText.ResetPassword,
        Actions.Delete        : KeyboardText.Delete,
        Actions.Rebuild       : KeyboardText.Rebuild,
        Actions.Update        : KeyboardText.UpdateServer,
        Actions.Reset         : KeyboardText.Reset
    }
    
    for i in range(0, len(actions), 2):
        row = []
        for action, text in list(actions.items())[i:i+2]:
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=ServerAction(action=action, server_id=server_id, confirm=False, image_id=0).pack()
                )
            )
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(
            text=KeyboardText.Back,
            callback_data=ServerList(action=Actions.Home).pack()
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def confirm_action_keyboard(action: str, server_id: int, image_id= int) -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(
                text=KeyboardText.Confirm,
                callback_data=ServerAction(action=action, server_id=server_id, confirm=True, image_id=image_id).pack()
            ),
            InlineKeyboardButton(
                text=KeyboardText.Cancel,
                callback_data=ServerAction(action=Actions.Info, server_id=server_id).pack()
            )
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def rebuild_keyboard(images: list[Image], server_id: int) -> InlineKeyboardMarkup:
    latest_images: dict[str, Image] = {}
    for image in images:
        if image.name not in latest_images or image.created > latest_images[image.name].created:
            latest_images[image.name] = image
    
    keyboard = []
    image_list = sorted(latest_images.values(), key=lambda x: x.name)

    for i in range(0, len(image_list), 2):
        row = []
        for j in range(i, min(i + 2, len(image_list))):
            image: Image = image_list[j]
            row.append(
                InlineKeyboardButton(
                    text=image.name,
                    callback_data=ServerAction(action=Actions.Rebuild, server_id=server_id, confirm=False, image_id=image.id).pack()
                )
            )
        keyboard.append(row)
    
    keyboard.append([
        InlineKeyboardButton(
            text=KeyboardText.Cancel,
            callback_data=ServerAction(action=Actions.Info, server_id=server_id).pack()
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
