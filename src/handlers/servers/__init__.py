from eiogram import Router
from . import menu, info, update, create


def setup_servers_handlers():
    router = Router()
    router.include_router(menu.router)
    router.include_router(info.router)
    router.include_router(update.router)
    router.include_router(create.router)
    return router
