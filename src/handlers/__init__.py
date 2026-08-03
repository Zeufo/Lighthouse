from aiogram import Router

from .commmon import router as common_router
from .digest import router as digest_router
from .registration import router as register_router
from .start_up import router as start_up_router
from .fallback import router as fallback_router

def get_main_router():
    main_router = Router()
    main_router.include_routers(common_router, start_up_router, register_router, digest_router, fallback_router)
    return main_router
