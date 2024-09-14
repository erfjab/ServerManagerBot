import json
from typing import Dict, Optional

from log import logger

# Configuration file path
CONFIG_FILE = 'data/.info.json'


class ConfigManager:
    _config: Optional[Dict] = None

    @staticmethod
    def _load_config() -> Optional[Dict]:
        """
        Load configuration from the JSON file.

        Returns:
            Optional[Dict]: The loaded configuration as a dictionary if successful, 
                             None if there was an error.
        """
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"JSON file '{CONFIG_FILE}' does not exist!")
            return None
        except json.JSONDecodeError:
            logger.error("Error decoding JSON file!")
            return None

    @staticmethod
    def get_config() -> Optional[Dict]:
        """
        Retrieve the configuration from the cache. 
        If not cached, load it from the file.

        Returns:
            Optional[Dict]: The configuration dictionary if successful, None otherwise.
        """
        if ConfigManager._config is None:
            ConfigManager._config = ConfigManager._load_config()
        return ConfigManager._config

    @staticmethod
    def get_admin_key(admin_chatid: int) -> Optional[str]:
        """
        Get the Hetzner API key for a specific admin chat ID.

        Args:
            admin_chatid (int): The chat ID of the admin.

        Returns:
            Optional[str]: The Hetzner API key if the admin chat ID exists, None otherwise.
        """
        config = ConfigManager.get_config()
        if config is None:
            return None
        chat_id_to_key = config.get('TELEGRAM_BOT_ADMINS', {})
        return chat_id_to_key.get(str(admin_chatid))

    @staticmethod
    def get_bot_token() -> Optional[str]:
        """
        Get the Telegram bot token.

        Returns:
            Optional[str]: The Telegram bot token if available, None otherwise.
        """
        config = ConfigManager.get_config()
        if config is None:
            return None
        return config.get('TELEGRAM_BOT_TOKEN')

    @staticmethod
    def get_all_admin_keys() -> Optional[Dict[int, str]]:
        """
        Get a dictionary of all admin chat IDs and their corresponding Hetzner API keys.

        Returns:
            Optional[Dict[int, str]]: A dictionary mapping admin chat IDs to Hetzner API keys,
                                       or None if configuration could not be loaded.
        """
        config = ConfigManager.get_config()
        if config is None:
            return None
        return config.get('TELEGRAM_BOT_ADMINS', {})

    @staticmethod
    def is_admin(chat_id: int) -> bool:
        """
        Check if a given chat ID is an admin.

        Args:
            chat_id (int): The chat ID to check.

        Returns:
            bool: True if the chat ID is an admin, False otherwise.
        """
        return str(chat_id) in ConfigManager.get_all_admin_keys()
