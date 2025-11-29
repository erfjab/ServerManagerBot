from enum import StrEnum


class Buttons(StrEnum):
    OWNER = "🌚 Owner"
    BACK = "🔙 Back"
    YES = "✅ Yes"
    NO = "❌ No"

    ### Clients
    CLIENTS_ADD = "➕ Add Client"
    CLIENTS_CHANGE_SECRET = "🔑 Change Secret"
    CLIENTS_CHANGE_REMARK = "✏️ Change Remark"
    CLIENTS_REMOVE = "❌ Remove Client"
    CLIENTS_SETTING = "⚙️ Client Settings"
    CLIENTS_CREATE = "🆕 Create Client"

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
    SERVERS_DEL_SNAPSHOT = "🗑️ Delete Snapshot"
    SERVERS_REMARK = "✏️ Change Remark"
    SERVERS_ASSIGN_IPV4 = "🔗 Assign IPv4"
    SERVERS_ASSIGN_IPV6 = "🔗 Assign IPv6"
    SERVERS_UNASSIGN_IPV4 = "❌ Unassign IPv4"
    SERVERS_UNASSIGN_IPV6 = "❌ Unassign IPv6"
    SERVERS_UPGRADE = "⬆️ Upgrade"

    ### Snapshots
    SNAPSHOTS = "📸 Snapshots"
    SNAPSHOTS_CREATE = "➕ Create Snapshot"
    SNAPSHOTS_RESTORE = "🔄 Restore Snapshot"
    SNAPSHOTS_DELETE = "🗑️ Delete Snapshot"
    SNAPSHOTS_REMARK = "✏️ Change Remark"

    ### Primary IPs
    PRIMARY_IPS = "🌐 Primary IPs"
    PRIMARY_IPS_CREATE = "➕ Create Primary IP"
    PRIMARY_IPS_ASSIGN = "🔗 Assign IP"
    PRIMARY_IPS_UNASSIGN = "❌ Unassign IP"
    PRIMARY_IPS_REMARK = "✏️ Change Remark"
    PRIMARY_IPS_DELETE = "🗑️ Delete IP"
    PRIMARY_IPS_CREATE_IPV4 = "➕ Create IPv4"
    PRIMARY_IPS_CREATE_IPV6 = "➕ Create IPv6"
