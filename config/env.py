from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvFileReader(BaseSettings):
    """env file reader"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_ADMINS: list[int] = []
    HETZNER_API_KEY: str = ""

    def is_admin(self, userid: int) -> bool:
        """check userid is admin or not"""
        return userid in self.TELEGRAM_ADMINS
