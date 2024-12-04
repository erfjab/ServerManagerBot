from aiogram.filters.callback_data import CallbackData


class ServerAction(CallbackData, prefix="server_action"):
    action: str
    server_id: int
    confirm: bool = False
    image_id: int = 0


class ServerList(CallbackData, prefix="server_list"):
    action: str


class ServerTypeSelect(CallbackData, prefix="server_type"):
    server: int = 0
    is_select: bool = False


class LocationTypeSelect(CallbackData, prefix="location_type"):
    location: int = 0
    is_select: bool = False


class ImageTypeSelect(CallbackData, prefix="image_type"):
    image: int = 0
    is_select: bool = False
