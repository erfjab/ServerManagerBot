from typing import List, Optional
from functools import wraps

from hcloud import Client
from hcloud.servers.domain import Server
from hcloud.actions.domain import Action
from hcloud.images.domain import Image
from hcloud import APIException, HCloudException
from hcloud.server_types.domain import ServerType
from hcloud.datacenters.domain import Datacenter

from utils import logger


def handle_hetzner_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIException as e:
            logger.error(
                f"Hetzner API Error in {func.__name__}: Code {e.code} - {e.message}"
            )
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
    async def get_servers(key: str) -> List[Server]:
        client = Client(token=key)
        return client.servers.get_all()

    @staticmethod
    @handle_hetzner_errors
    async def get_server(key: str, server_id: int) -> Optional[Server]:
        client = Client(token=key)
        return client.servers.get_by_id(server_id)

    @staticmethod
    @handle_hetzner_errors
    async def get_server_type(key: str, server_id: int) -> Optional[ServerType]:
        client = Client(token=key)
        return client.server_types.get_by_id(server_id)

    @staticmethod
    @handle_hetzner_errors
    async def power_on(key: str, server: Server) -> Optional[Action]:
        client = Client(token=key)
        return client.servers.power_on(server)

    @staticmethod
    @handle_hetzner_errors
    async def power_off(key: str, server: Server) -> Optional[Action]:
        client = Client(token=key)
        return client.servers.power_off(server)

    @staticmethod
    @handle_hetzner_errors
    async def reboot(key: str, server: Server) -> Optional[Action]:
        client = Client(token=key)
        return client.servers.reboot(server)

    @staticmethod
    @handle_hetzner_errors
    async def reset_password(key: str, server: Server) -> Optional[str]:
        client = Client(token=key)
        return client.servers.reset_password(server).root_password

    @staticmethod
    @handle_hetzner_errors
    async def delete(key: str, server: Server) -> Optional[Action]:
        client = Client(token=key)
        return client.servers.delete(server)

    @staticmethod
    @handle_hetzner_errors
    async def reset(key: str, server: Server) -> Optional[Action]:
        client = Client(token=key)
        return client.servers.reset(server)

    @staticmethod
    @handle_hetzner_errors
    async def get_images(key: str, arch: str = None) -> List[Image]:
        client = Client(token=key)
        return client.images.get_all(architecture=arch)

    @staticmethod
    @handle_hetzner_errors
    async def rebuild_server(
        key: str, server: Server, image_id: int
    ) -> Optional[Action]:
        client = Client(token=key)
        image = client.images.get_by_id(image_id)
        return client.servers.rebuild(server, image)

    @staticmethod
    @handle_hetzner_errors
    async def create_server(
        key: str,
        name: str,
        server_type: ServerType,
        image: Image,
        datacenter: Datacenter,
    ) -> Optional[Server]:
        client = Client(token=key)
        server = client.servers.create(
            name=name, server_type=server_type, image=image, datacenter=datacenter
        )
        return server.server

    @staticmethod
    @handle_hetzner_errors
    async def get_image(key: str, id: int) -> Optional[Image]:
        client = Client(token=key)
        return client.images.get_by_id(id)

    @staticmethod
    @handle_hetzner_errors
    async def get_server_types(key: str) -> List[ServerType]:
        client = Client(token=key)
        return client.server_types.get_all()

    @staticmethod
    @handle_hetzner_errors
    async def get_datacenters(key: str) -> List[Datacenter]:
        client = Client(token=key)
        return client.datacenters.get_all()

    @staticmethod
    @handle_hetzner_errors
    async def get_datacenter(key: str, id: int) -> Optional[Datacenter]:
        client = Client(token=key)
        return client.datacenters.get_by_id(id)
