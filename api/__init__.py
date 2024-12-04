from .hetzner import HetznerManager
from config import EnvFile

HetznerAPI = HetznerManager(key=EnvFile.HETZNER_API_KEY)

__all__ = ["HetznerAPI"]
