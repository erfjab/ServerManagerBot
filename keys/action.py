from enum import Enum


class Actions(str, Enum):
    POWER_ON = "power_on"
    POWER_OFF = "power_off"
    REBOOT = "reboot"
    RESET_PASSWORD = "reset_password"
    DELETE = "delete"
    HOME = "home"
    INFO = "info"
    REBUILD = "rebuild"
    UPDATE = "update"
    RESET = "reset"
