from eiogram import Router
from . import base
from .middlewares import Middleware
from .clients import setup_clients_handlers


def setup_handlers() -> Router:
    router = Router()
    router.middleware.register(Middleware())
    router.include_router(base.router)
    router.include_router(setup_clients_handlers())
    return router


__all__ = ["setup_handlers"]
