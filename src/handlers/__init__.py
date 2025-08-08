from eiogram import Router
from . import commands
from .middlewares import Middleware


def setup_handlers() -> Router:
    router = Router()
    router.middleware.register(Middleware())
    router.include_router(commands.router)
    return router


__all__ = ["setup_handlers"]
