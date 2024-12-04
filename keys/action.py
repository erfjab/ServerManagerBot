from enum import Enum


class Actions(str, Enum):
    POWER_ON = "power on"
    POWER_OFF = "power off"
    REBOOT = "reboot"
    RESET_PASSWORD = "reset password"
    DELETE = "delete"
    HOME = "home"
    INFO = "info"
    REBUILD = "rebuild"
    UPDATE = "update"
    RESET = "reset"
