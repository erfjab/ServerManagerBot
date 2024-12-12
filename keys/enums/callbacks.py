from enum import Enum


class Actions(str, Enum):
    HOME = "home"
    LIST = "list"
    INFO = "info"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class Pages(str, Enum):
    HOME = "home"
    MENU = "menu"
    SERVER = "server"
