from fastapi import APIRouter
from . import base, telegram


def setup_api_routers() -> APIRouter:
    router = APIRouter()
    router.include_router(base.router)
    router.include_router(telegram.router)
    return router


__all__ = ["setup_api_routers"]
