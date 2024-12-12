from aiogram.filters.callback_data import CallbackData
from .enums import Pages, Actions, ServerCreate, ServerUpdate


class PageCB(CallbackData, prefix="pages"):
    key: str = "KEY"
    page: Pages | None = None
    action: Actions | ServerUpdate | None = None
    server_id: int | None = None
    image_id: int | None = None
    confirm: bool = False


class SelectCB(CallbackData, prefix="select"):
    key: str = "KEY"
    page: Pages | None = None
    action: Actions | None = None
    datatype: ServerCreate | None = None
    datavalue: str | int | None = None
