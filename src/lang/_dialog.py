from enum import StrEnum


class Dialogs(StrEnum):
    ### Commands
    COMMAND_START = "<b>🌟 Welcome! I'm your Server Management Assistant</b>"

    ### Actions
    ACTIONS_SUCCESS = "<b>🎉✅ Action completed successfully.</b>"
    ACTIONS_FAILED = "<b>⚠️❌ Action failed.</b>"
    ACTIONS_CONFIRM = "<b>❓ Are you sure you want to proceed?</b>\n🔘 Please approve to continue or cancel to go back."
    ACTIONS_CANCELLED = "<b>🚫❌ Action cancelled.</b>\n↩️ Go back to the previous menu."
    ACTIONS_DUPLICATE = "<b>⚠️❌ A item with this remark already exists.</b>\n\n🔄 Please choose a different remark."
    ACTIONS_WAITING = "<b>⏳ Please wait...</b>"

    ### Clients
    CLIENTS_MENU = "<b>👥 Clients Menu</b>\n👇 Select an action from the menu below."
    CLIENTS_ENTER_REMARK = "✏️ Enter a remark for the client:"
    CLIENTS_ENTER_SECRET = "🔑 Enter client secret [api key]:"
    CLIENTS_NOT_FOUND = "<b>🔍❌ Client not found.</b>"
    CLIENTS_CREATION_SUCCESS = "<b>🎉✅ Client created successfully.</b>\n⚙️ You can now manage the client."
    CLIENTS_INVALID_TOKEN = "<b>⚠️❌ Invalid client secret [api key].</b>\n🔍 Please check the token and try again."
    CLIENTS_INFO = "<b>👤 Client Setting</b>\n\n🔑 <b>API Key:</b> <tg-spoiler>{secret}</tg-spoiler>"

    ### Servers
    SERVERS_MENU = "<b>🖥️ Servers Menu</b>\n👇 Select an action from the menu below."
    SERVERS_NOT_FOUND = "🔍❌ Not found server."
    SERVERS_ACCESS_GRANT_PROMPT = "✏️ Enter the Chat ID to grant access:"
    SERVERS_ACCESS_REVOKE_PROMPT = "✏️ Enter the Chat ID to revoke access:"
    SERVERS_ACCESS_LIST = "<b>📋 Access List:</b>\n{list}"
    SERVERS_ACCESS_GRANTED = "<b>🎉✅ Access granted to {chat_id}.</b>"
    SERVERS_ACCESS_REVOKED = "<b>🎉✅ Access revoked from {chat_id}.</b>"
    SERVERS_ACCESS_ALREADY_EXISTS = "<b>⚠️❌ Access already exists for {chat_id}.</b>"
    SERVERS_ACCESS_NOT_FOUND = "<b>⚠️❌ Access not found for {chat_id}.</b>"
    SERVERS_INFO = """
<b>🚀 Name:</b> <code>{name}</code> [<code>{status}</code>]
<b>🔗 IPV4:</b> <code>{ipv4}</code>
<b>🔗 IPV6:</b> <code>{ipv6}</code>
<b>🌍 County:</b> <code>{country}, {city}</code>
<b>⚙️ Cpu:</b> <code>{cpu} Core</code>
<b>💾 Ram:</b> <code>{ram} GB</code>
<b>💿 Disk:</b> <code>{disk} GB</code>
<b>📸 Snapshots:</b> <code>{snapshot}</code>
<b>🖼️ Image:</b> <code>{image}</code>
<b>📊 Traffic:</b>
 • In: <code>{traffic_in} GB</code>
 • Out: <code>{traffic_out} GB</code>
 • Total: <code>{traffic_total} GB</code>
 • Included: <code>{traffic_included} GB</code>
 • Used: <code>{traffic_used_percent}% [Out/Included traffic]</code>
 • Billable: <code>{traffic_billable} GB</code>
<b>💰 Price:</b>
 • Hourly: <code>{price_hourly}</code>
 • Monthly: <code>{price_monthly}</code>
<b>📅 Created:</b> <code>{created}</code> [<code>{created_day} days ago</code>]
"""
    SERVERS_REBUILD_CONFIRM = "<b>⚠️ Are you sure you want to rebuild the server?</b>\n🧹 This action will erase all data on the server.\n🖼️ Please select an image to proceed."
    SERVERS_IMAGES_NOT_FOUND = "🔍❌ Not found image."
    SERVERS_ENTER_REMARK = "✏️ Enter a remark for the server:"
    SERVERS_SELECT_DATACENTER = "🌍 Select a datacenter for the server:"
    SERVERS_SELECT_PLAN = "💰 Select a plan for the server:"
    SERVERS_SELECT_IMAGE = "🖼️ Select an image for the server:"
    SERVERS_DATACENTERS_NOT_FOUND = "🔍❌ Not found datacenter."
    SERVERS_PLANS_NOT_FOUND = "🔍❌ No plans found for this location."
    SERVERS_CREATION_SUCCESS = "<b>🎉✅ Server created successfully.</b>\n⚙️ You can now manage the server."
    SERVERS_CREATION_FAILED = "⚠️❌ Server creation failed."
    SERVERS_PASSWORD_RESET_SUCCESS = "🎉✅ Server password reset successfully.\n🔑 Your new password: <code>{password}</code>"
    SERVERS_SNAPSHOT_DELETE_CONFIRM = (
        "<b>⚠️ Are you sure you want to delete the snapshot?</b>\n🗑️ This action cannot be undone. select a snapshot to delete."
    )
    SERVERS_SNAPSHOT_NOT_FOUND = "🔍❌ Not found snapshot."
    SERVERS_PRIMARY_IPS_NOT_FOUND = "🔍❌ Not found primary IPs."
    SERVERS_ASSIGN_SELECT = "🌍 Select a primary IP to assign to the server:"
    SERVERS_ASSIGN_UNASSIGN_IPV4 = "🔗 First Unassign IPv4"
    SERVERS_ASSIGN_UNASSIGN_IPV6 = "🔗 First Unassign IPv6"
    SERVERS_REMARK_VALIDATION = (
        "<b>⚠️❌ Invalid remark format.</b>\n🔍 Please enter a valid remark without special characters and space."
    )
    SERVERS_UPGRADE_SELECT = "⬆️ Select a plan to upgrade the server:\n\n<b>Current:</b> <code>{current_plan}</code>"
    SERVERS_UPGRADE_NOT_FOUND = "🔍❌ No upgrade plans available for this server."
    SERVERS_UPGRADE_SUCCESS = "<b>🎉✅ Server upgraded successfully.</b>"
    SERVERS_SHOULD_BE_OFF = "⚠️❌ Please power off the server and try again."

    ### Snapshots
    SNAPSHOTS_MENU = "<b>📸 Snapshots Menu</b>\n👇 Select an action from the menu below."
    SNAPSHOTS_NOT_FOUND = "<b>🔍❌ Not found snapshot.</b>"
    SNAPSHOTS_INFO = """
<b>📸 Name:</b> <code>{name}</code>
<b>🔗 Status:</b> <code>{status}</code>
<b>💾 Size:</b> <code>{size} GB</code>
<b>📅 Created:</b> <code>{created}</code> [<code>{created_day} days ago</code>]
"""
    SNAPSHOTS_ENTER_REMARK = "✏️ Enter a remark for the snapshot:"
    SNAPSHOTS_SERVERS_NOT_FOUND = "🔍❌ Not found servers for the snapshot."
    SNAPSHOTS_SELECT_SERVER = "🌍 Select a server for the snapshot:"
    SNAPSHOTS_SERVER_NOT_FOUND = "🔍❌ Server not found."
    SNAPSHOTS_CREATE_SUCCESS = "<b>🎉✅ Snapshot created successfully.</b>"
    SNAPSHOTS_UPDATE_SUCCESS = "<b>🎉✅ Snapshot updated successfully.</b>"
    SNAPSHOTS_DELETE_SUCCESS = "<b>🎉✅ Snapshot deleted successfully.</b>"

    ### Primary IPs
    PRIMARY_IPS_MENU = "<b>🌐 Primary IPs Menu</b>\n👇 Select an action from the menu below."
    PRIMARY_IPS_NOT_FOUND = "🔍❌ Not found primary IP."
    PRIMARY_IPS_INFO = """
<b>🌐 Name:</b> <code>{name}</code>
<b>🔗 IP:</b> <code>{ip}</code>
<b>🔗 Assignee:</b> <code>{assignee}</code>
<b>🔗 Assignee ID:</b> <code>{assignee_id}</code>
<b>📅 Created:</b> <code>{created}</code> [<code>{created_day} days ago</code>]
"""
    PRIMARY_IP_NOT_FOUND = "🔍❌ Not found primary IP."
    PRIMARY_IP_ENTER_REMARK = "✏️ Enter a remark for the primary IP:"
    PRIMARY_IPS_UPDATE_SUCCESS = "<b>🎉✅ Primary IP updated successfully.</b>"
    PRIMARY_IP_ASSIGNEE_NOT_FOUND = "🔍❌ Not found primary IP assignee."
    PRIMARY_IP_SELECT_ASSIGNEE = "🌍 Select a server to assign the primary IP:"
    PRIMARY_IPS_ENTER_REMARK = "✏️ Enter a remark for the primary IP:"
    PRIMARY_IPS_CREATE_FAILED = "⚠️❌ Primary IP creation failed."
    PRIMARY_IPS_CREATE_SUCCESS = "<b>🎉✅ Primary IP created successfully.</b>"
    PRIMARY_IPS_NO_DATACENTERS = "🔍❌ No datacenters found."
    PRIMARY_IPS_SELECT_DATACENTER = "🌍 Select a datacenter for the primary IP:"

    ### Traffic Monitor
    TRAFFIC_ALERT = (
        "<b>⚠️ Traffic Alert</b>\n"
        "<b>Client:</b> <code>{client}</code>\n"
        "<b>Server:</b> <code>{server_name}</code> [<code>{server_id}</code>]\n"
        "<b>Outgoing:</b> <code>{out} GB</code> <b>of</b> <code>{included} GB</code>\n"
        "<b>Used:</b> <code>{percent}%</code>\n"
        "<b>Billable:</b> <code>{billable} GB</code>"
    )
