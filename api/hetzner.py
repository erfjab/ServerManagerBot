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
    def __init__(self, key: str) -> None:
        self.client = Client(token=key)

    @handle_hetzner_errors
    async def get_servers(self) -> List[Server]:
        return self.client.servers.get_all()

    @handle_hetzner_errors
    async def get_server(self, server_id: int) -> Optional[Server]:
        return self.client.servers.get_by_id(server_id)

    @handle_hetzner_errors
    async def get_server_type(self, server_id: int) -> Optional[ServerType]:
        return self.client.server_types.get_by_id(server_id)

    @handle_hetzner_errors
    async def power_on(self, server: Server) -> Optional[Action]:
        return self.client.servers.power_on(server)

    @handle_hetzner_errors
    async def power_off(self, server: Server) -> Optional[Action]:
        return self.client.servers.power_off(server)

    @handle_hetzner_errors
    async def reboot(self, server: Server) -> Optional[Action]:
        return self.client.servers.reboot(server)

    @handle_hetzner_errors
    async def reset_password(self, server: Server) -> Optional[str]:
        return self.client.servers.reset_password(server).root_password

    @handle_hetzner_errors
    async def delete(self, server: Server) -> Optional[Action]:
        return self.client.servers.delete(server)

    @handle_hetzner_errors
    async def reset(self, server: Server) -> Optional[Action]:
        return self.client.servers.reset(server)

    @handle_hetzner_errors
    async def get_images(self, arch: str = None) -> List[Image]:
        return self.client.images.get_all(architecture=arch)

    @handle_hetzner_errors
    async def rebuild_server(self, server: Server, image_id: int) -> Optional[Action]:
        image = self.client.images.get_by_id(image_id)
        return self.client.servers.rebuild(server, image)

    @handle_hetzner_errors
    async def create_server(
        self, name: str, server_type: ServerType, image: Image
    ) -> Optional[Server]:
        server = self.client.servers.create(
            name=name, server_type=server_type, image=image
        )
        return server.server

    async def get_image(self, id: int) -> Optional[Image]:
        return self.client.images.get_by_id(id)

    @handle_hetzner_errors
    async def get_server_types(self) -> List[ServerType]:
        return self.client.server_types.get_all()

    @handle_hetzner_errors
    async def get_datacenters(self) -> List[Datacenter]:
        return self.client.datacenters.get_all()

    @handle_hetzner_errors
    async def get_datacenter(self, id: int) -> Optional[Datacenter]:
        return self.client.datacenters.get_by_id(id)
