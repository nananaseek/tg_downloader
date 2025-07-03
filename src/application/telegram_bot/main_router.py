from aiogram import Router
from .super_groupe import super_groups_router
from .commands import command_router
from .chat import chat_router


main_router = Router()
main_router.include_routers(
    super_groups_router,
    command_router,
    chat_router
)