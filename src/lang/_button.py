from enum import StrEnum


class Buttons(StrEnum):
    OWNER = "Owner"
    SERVERS = "Servers"
    PRIMARY_IPS = "Primary IPs"
    SNAPSHOTS = "SnapShots"
    CLIENTS_ADD = "Add Client"
    CLIENTS_CHANGE_SECRET = "Change Secret"
    CLIENTS_CHANGE_REMARK = "Change Remark"
    CLIENTS_REMOVE = "Remove Client"
    BACK = "Back"
    CREATE_CREATE = "Create Client"
    YES = "Yes"
    NO = "No"
