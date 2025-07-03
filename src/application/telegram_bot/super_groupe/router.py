from aiogram import Router

from .handlers import activation_router, monitoring_router


super_groups_router = Router()

super_groups_router.include_routers(
    activation_router,
    monitoring_router
)