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
