from aiogram.filters.callback_data import CallbackData


class ServerAction(CallbackData, prefix='server_action'):
    action: str
    server_id: int
    confirm: bool = False
    image_id: int = 0


class ServerList(CallbackData, prefix='server_list'):
    action: str
