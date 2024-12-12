from pydantic_settings import BaseSettings, SettingsConfigDict


class MessageTextsFile(BaseSettings):
    """Message texts used in the bot."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    START: str = "👋 Welcome to ServerManagerBot\nDevelop and Design by @ErfJabs"
    MENU: str = "🗃️ Your Account Menu:"
    SERVER_LIST: str = "🖥️ Here are your servers:"
    IS_UPDATED: str = "✅ is updated!"
    SERVER_INFO: str = (
        "<b>{status_emoji} Name:</b> <code>{name}</code> [<code>{status}</code>]\n"
        "<b>🔗 IPV4:</b> <code>{ipv4}</code>\n"
        "<b>🔗 IPV6:</b> <code>{ipv6}</code>\n"
        "<b>🏛️ County:</b> <code>{country}, {city}</code>\n"
        "<b>⚙️ Cpu:</b> <code>{cpu} Core</code>\n"
        "<b>🗂️ Ram:</b> <code>{ram} GB</code>\n"
        "<b>🗃️ Disk:</b> <code>{disk} GB</code>\n"
        "<b>🎟️ Image:</b> <code>{image}</code>\n"
        "<b>⚡ Traffic:</b> <code>{traffic} GB</code>\n"
        "<b>📅 Created:</b> <code>{created}</code> [<code>{created_day} days ago</code>]\n"
        "<b>🔑 Password:</b> <code>{password}</code>"
    )
    NOT_FOUND: str = "❗ Not Found! (check logs)"
    TRY_AGAIN: str = "⚠️ Oops! An error occurred, please try again..."
    CHECK_LOGS: str = "⚠️ Oops! An error occurred, please check the logs."
    CONFIRM_ACTION: str = "Are you sure you want to <b>{action}</b> this server?"
    IMAGE_LIST: str = "🖼️ Select your image:"
    WAIT: str = "⏳ Please wait..."
    SELECT_SERVER_TYPE: str = "🗃️ Select Server:\nC: Core\nM: Memory\nP: Monthly Price"
    SELECT_LOCATION_TYPE: str = "👀 Select location:"
    SELECT_IMAGE_TYPE: str = "🖼️ Select image:"
    SERVER_CREATED: str = "✅ is created!"
