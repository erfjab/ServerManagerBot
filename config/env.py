import hashlib
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvFileReader(BaseSettings):
    """env file reader"""

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_ADMINS: list[int] = []
    HETZNER_API_KEYS: list[tuple[str, str]] = []

    def is_admin(self, userid: int) -> bool:
        """check userid is admin or not"""
        return userid in self.TELEGRAM_ADMINS

    def to_hash(self, key: str, length: int = 4) -> str:
        """create a hash from key"""
        hash_object = hashlib.md5(key.encode())
        full_hash = hash_object.hexdigest()
        return full_hash[:length]

    def from_hash(self, hashkey: str, length: int = 4) -> str:
        """create a key from hash"""
        for key_pair in self.HETZNER_API_KEYS:
            current_hash = self.to_hash(key_pair[1])
            if current_hash == hashkey:
                return key_pair[1]
        return None
