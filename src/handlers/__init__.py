from eiogram import Router
from . import base, fallback  # noqa
from .middlewares import Middleware
from .clients import setup_clients_handlers
from .servers import setup_servers_handlers
from .snapshots import setup_snapshots_handlers


def setup_handlers() -> Router:
    router = Router()
    router.middleware.register(Middleware())
    router.include_router(base.router)
    router.include_router(setup_clients_handlers())
    router.include_router(setup_servers_handlers())
    router.include_router(setup_snapshots_handlers())
    return router


__all__ = ["setup_handlers"]
