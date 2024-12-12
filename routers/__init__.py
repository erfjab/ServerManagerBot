from aiogram import Router
from . import base
from .server import setup_server_routers

__all__ = ["setup_routers", "base"]


def setup_routers() -> Router:
    router = Router()

    router.include_router(setup_server_routers())
    router.include_router(base.router)

    return router
