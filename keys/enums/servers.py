from enum import Enum


class ServerCreate(str, Enum):
    LOCATION = "location"
    SERVER = "server"
    IMAGE = "image"


class ServerUpdate(str, Enum):
    POWER_ON = "power_on"
    POWER_OFF = "power_off"
    REBOOT = "reboot"
    RESET_PASSWORD = "reset_password"
    DELETE = "delete"
    REBUILD = "rebuild"
    RESET = "reset"
    UPDATE = "update"
