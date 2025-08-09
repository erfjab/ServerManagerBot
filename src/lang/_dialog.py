from enum import StrEnum


class Dialogs(StrEnum):
    ### Commands
    COMMAND_START = "<b>☄️ Hi Dear.</b>"

    ### Actions
    ACTIONS_SUCCESS = "<b>✅ Action completed successfully.</b>"
    ACTIONS_FAILED = "<b>❌ Action failed.</b>"
    ACTIONS_CONFIRM = "<b>Are you sure you want to proceed?</b>\nPlease approve to continue or cancel to go back."
    ACTIONS_CANCELLED = "<b>❌ Action cancelled.</b>\ngo back to the previous menu."
    ACTIONS_DUPLICATE = "<b>❌ A item with this remark already exists.</b>\n\nPlease choose a different remark."

    ### Clients
    CLIENTS_MENU = "<b>Clients Menu</b>\nSelect an action from the menu below."
    CLIENTS_ENTER_REMARK = "Enter a remark for the client:"
    CLIENTS_ENTER_SECRET = "Enter client secret [api key]:"
    CLIENTS_NOT_FOUND = "<b>❌ Client not found.</b>"
    CLIENTS_CREATION_SUCCESS = "<b>✅ Client created successfully.</b>\nYou can now manage the client."
    CLIENTS_INVALID_TOKEN = "<b>❌ Invalid client secret [api key].</b>\nPlease check the token and try again."

    ### Servers
    SERVERS_MENU = "<b>Servers Menu</b>\nSelect an action from the menu below."
    SERVERS_NOT_FOUND = "<b>❌ Not found server.</b>"
    SERVERS_INFO = """
<b>🚀 Name:</b> <code>{name}</code> [<code>{status}</code>]
<b>🔗 IPV4:</b> <code>{ipv4}</code>
<b>🔗 IPV6:</b> <code>{ipv6}</code>
<b>🏛️ County:</b> <code>{country}, {city}</code>
<b>⚙️ Cpu:</b> <code>{cpu} Core</code>
<b>🗂️ Ram:</b> <code>{ram} GB</code>
<b>🗃️ Disk:</b> <code>{disk} GB</code>
<b>📸 Snapshots:</b> <code>{snapshot}</code>
<b>🎟️ Image:</b> <code>{image}</code>
<b>⚡ Traffic:</b> <code>{traffic} GB</code>
<b>📅 Created:</b> <code>{created}</code> [<code>{created_day} days ago</code>]
"""
    SERVERS_REBUILD_CONFIRM = "<b>Are you sure you want to rebuild the server?</b>\nThis action will erase all data on the server.\nPlease select an image to proceed."
    SERVERS_IMAGES_NOT_FOUND = "❌ Not found image."
    SERVERS_ENTER_REMARK = "Enter a remark for the server:"
    SERVERS_SELECT_DATACENTER = "Select a datacenter for the server:"
    SERVERS_SELECT_PLAN = "Select a plan for the server:"
    SERVERS_SELECT_IMAGE = "Select an image for the server:"
    SERVERS_DATACENTERS_NOT_FOUND = "❌ Not found datacenter."
    SERVERS_PLANS_NOT_FOUND = "❌ No plans found for this location."
    SERVERS_CREATION_SUCCESS = "<b>✅ Server created successfully.</b>\nYou can now manage the server."
    SERVERS_CREATION_FAILED = "❌ Server creation failed."
    SERVERS_PASSWORD_RESET_SUCCESS = "✅ Server password reset successfully.\nYour new password: <code>{password}</code>"
    SERVERS_SNAPSHOT_DELETE_CONFIRM = (
        "<b>Are you sure you want to delete the snapshot?</b>\nThis action cannot be undone. select a snapshot to delete."
    )
    SERVERS_SNAPSHOT_NOT_FOUND = "❌ Not found snapshot."
