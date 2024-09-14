from typing import List, Optional
from hcloud import Client
from hcloud.servers.domain import Server
from hcloud.actions.domain import Action
from hcloud.images.domain import Image
from config import ConfigManager
from log import logger
from functools import wraps
from hcloud import APIException, HCloudException

def handle_hetzner_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIException as e:
            logger.error(f"Hetzner API Error in {func.__name__}: Code {e.code} - {e.message}")
        except HCloudException as e:
            logger.error(f"Hetzner Client Error in {func.__name__}: {str(e)}")
        except ValueError as e:
            logger.error(f"Value Error in {func.__name__}: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
        return None
    return wrapper

class HetznerManager:

    @staticmethod
    @handle_hetzner_errors
    async def _get_client(admin_chatid: int) -> Optional[Client]:
        api_key = ConfigManager.get_admin_key(admin_chatid)
        if not api_key:
            raise ValueError(f"No Hetzner API key found for chat ID: {admin_chatid}")
        return Client(token=api_key)

    @staticmethod
    @handle_hetzner_errors
    async def get_servers(admin_chatid: int) -> List[Server]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.get_all()

    @staticmethod
    @handle_hetzner_errors
    async def get_server(server_id: int, admin_chatid: int) -> Optional[Server]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.get_by_id(server_id)

    @staticmethod
    @handle_hetzner_errors
    async def power_on(server: Server, admin_chatid: int) -> Optional[Action]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.power_on(server)

    @staticmethod
    @handle_hetzner_errors
    async def power_off(server: Server, admin_chatid: int) -> Optional[Action]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.power_off(server)

    @staticmethod
    @handle_hetzner_errors
    async def reboot(server: Server, admin_chatid: int) -> Optional[Action]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.reboot(server)

    @staticmethod
    @handle_hetzner_errors
    async def reset_password(server: Server, admin_chatid: int) -> Optional[str]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.reset_password(server).root_password

    @staticmethod
    @handle_hetzner_errors
    async def delete(server: Server, admin_chatid: int) -> Optional[Action]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.delete(server)

    @staticmethod
    @handle_hetzner_errors
    async def reset(server: Server, admin_chatid: int) -> Optional[Action]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.servers.reset(server)

    @staticmethod
    @handle_hetzner_errors
    async def get_images(admin_chatid: int) -> List[Image]:
        client = await HetznerManager._get_client(admin_chatid)
        return client.images.get_all()

    @staticmethod
    @handle_hetzner_errors
    async def rebuild_server(server: Server, image_id: int, admin_chatid: int) -> Optional[Action]:
        client = await HetznerManager._get_client(admin_chatid)
        image = client.images.get_by_id(image_id)
        return client.servers.rebuild(server, image)
