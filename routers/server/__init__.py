from aiogram import Router

from . import menu, data, create, edit

__all__ = ["setup_server_routers", "menu", "data", "create", "edit"]


def setup_server_routers() -> Router:
    router = Router()

    router.include_router(data.router)
    router.include_router(menu.router)
    router.include_router(edit.router)
    router.include_router(create.router)

    return router
