from pydantic_settings import BaseSettings, SettingsConfigDict


class KeyboardTextsFile(BaseSettings):
    """Keyboard texts used in the bot."""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    UPDATE: str = "🔄 Update"
    POWER_ON: str = "🟢 Power On"
    POWER_OFF: str = "🔴 Power Off"
    REBOOT: str = "🔄 Reboot"
    RESET_PASSWORD: str = "🔑 Reset Password"
    DELETE: str = "🗑️ Delete"
    BACK: str = "⬅️ Back"
    CONFIRM: str = "✅ Confirm"
    CANCEL: str = "❌ Cancel"
    REBUILD: str = "🔧 Rebuild"
    UPDATE_SERVER: str = "🔄 Update Info"
    RESET: str = "🔄 Reset"
    HETZNER: str = "🟥 Hetzner"
    CREATE: str = "➕ Create"
    SERVERS: str = "☁️ Servers"
    HOMES: str = "🏛️ Home"
