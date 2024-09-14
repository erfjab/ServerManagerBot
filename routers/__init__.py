from aiogram import Router

from . import server

def setup_routers() -> Router:

    from . import (
        base
    )

    router = Router()

    router.include_router(base.router)
    router.include_router(server.router)

    return router