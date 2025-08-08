from enum import StrEnum
from eiogram.utils.callback_data import CallbackData


class AreaType(StrEnum):
    HOME = "hm"


class TaskType(StrEnum):
    MENU = "mn"
    LIST = "ls"
    CREATE = "cr"
    INFO = "nf"
    UPDATE = "pt"


class StepType(StrEnum): ...


class BotCB(CallbackData, prefix="x"):
    area: AreaType = AreaType.HOME
    task: TaskType = TaskType.MENU
    step: StepType | None = None
    page: int = 0
    is_approve: bool = False
    target: str | int = 0
