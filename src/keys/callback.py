from enum import StrEnum
from eiogram.utils.callback_data import CallbackData


class AreaType(StrEnum):
    HOME = "hm"
    CLIENT = "cl"
    SNAPSHOT = "ss"
    PRIMARY_IP = "pi"
    SERVER = "sv"


class TaskType(StrEnum):
    MENU = "mn"
    LIST = "ls"
    CREATE = "cr"
    INFO = "nf"
    UPDATE = "pt"


class StepType(StrEnum):
    CHANGE_REMARK = "cr"
    CHANGE_SECRET = "cs"
    REMOVE_CLIENT = "rmc"
    SERVERS_REBOOT = "reb"
    SERVERS_REBUILD = "rbl"
    SERVERS_POWER_ON = "pwn"
    SERVERS_POWER_OFF = "pwf"
    SERVERS_RESET_PASSWORD = "rsp"
    SERVERS_RESET = "rst"
    SERVERS_REMOVE = "rms"
    SERVERS_CREATE_SNAPSHOT = "crs"
    SERVERS_DEL_SNAPSHOT = "dsp"
    SERVERS_REMARK = "srv"
    SERVERS_UNASSIGN_IPV4 = "sua4"
    SERVERS_UNASSIGN_IPV6 = "sua6"
    SERVERS_ASSIGN_IPV4 = "saa4"
    SERVERS_ASSIGN_IPV6 = "saa6"
    SNAPSHOTS_RESTORE = "srs"
    SNAPSHOTS_DELETE = "sds"
    SNAPSHOTS_REMARK = "srm"
    PRIMARY_IPS_ASSIGN = "pia"
    PRIMARY_IPS_UNASSIGN = "pua"
    PRIMARY_IPS_REMARK = "pir"
    PRIMARY_IPS_DELETE = "pid"


class BotCB(CallbackData, prefix="x"):
    area: AreaType = AreaType.HOME
    task: TaskType = TaskType.MENU
    step: StepType | None = None
    page: int = 0
    is_approve: bool = False
    target: str | int = 0
