from eiogram import Router
from . import menu, create, update


def setup_clients_handlers():
    router = Router()
    router.include_router(menu.router)
    router.include_router(create.router)
    router.include_router(update.router)
    return router
