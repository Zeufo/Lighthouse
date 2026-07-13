from aiogram import Router

from .start_up import router as start_up_router


def get_main_router():
    main_router = Router()
    main_router.include_routers(start_up_router)

    return main_router
