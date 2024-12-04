from aiogram import Router
from . import base, data, edit, create

__all__ = ["setup_routers", "base", "data", "edit", "create"]


def setup_routers() -> Router:
    router = Router()

    router.include_router(base.router)
    router.include_router(data.router)
    router.include_router(edit.router)
    router.include_router(create.router)

    return router
