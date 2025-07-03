import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.settings.config import settings

from .lifespan import on_startup, on_shutdown

from src.application.telegram_bot import (
    main_router,
    ChatService,
    UserServices,
)


logger = logging.getLogger(__name__)


async def start_bot() -> None:
    dp = Dispatcher()
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    chat_service = ChatService()
    user_service = UserServices()

    dp["chat_service"] = chat_service
    dp["user_service"] = user_service

    dp.include_router(main_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await dp.start_polling(bot)