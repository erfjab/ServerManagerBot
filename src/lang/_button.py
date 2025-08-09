from enum import StrEnum


class Buttons(StrEnum):
    OWNER = "🌚 Owner"
    PRIMARY_IPS = "🌐 Primary IPs"
    SNAPSHOTS = "📸 SnapShots"
    CLIENTS_ADD = "➕ Add Client"
    CLIENTS_CHANGE_SECRET = "🔑 Change Secret"
    CLIENTS_CHANGE_REMARK = "✏️ Change Remark"
    CLIENTS_REMOVE = "❌ Remove Client"
    BACK = "🔙 Back"
    CREATE_CREATE = "🆕 Create Client"
    YES = "✅ Yes"
    NO = "❌ No"

    ### Servers
    SERVERS = "🖥️ Servers"
    SERVERS_REBOOT = "🔄 Reboot"
    SERVERS_REBUILD = "🛠️ Rebuild"
    SERVERS_POWER_ON = "⚡ Power On"
    SERVERS_POWER_OFF = "🔌 Power Off"
    SERVERS_RESET_PASSWORD = "🔓 Reset Password"
    SERVERS_RESET = "🔄 Reset"
    SERVERS_REMOVE = "🗑️ Remove Server"
    SERVERS_CREATE = "➕ Create Server"
    SERVERS_CREATE_SNAPSHOT = "📷 Create Snapshot"
    SERVERS_DEL_SNAPSHOT = "❌ Delete Snapshot"
