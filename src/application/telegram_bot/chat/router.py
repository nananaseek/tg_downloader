from aiogram import Router

from .filters import PrivateFilter

from .handlers import start_router, monitoring_router

chat_router = Router()

chat_router.message.filter(PrivateFilter())
chat_router.include_routers(
    start_router, 
    monitoring_router
)