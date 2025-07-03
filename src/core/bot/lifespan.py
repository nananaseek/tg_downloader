import os
import logging

from aiogram import Bot

from src.settings.config import settings

from src.application.telegram_bot import ChatService, UserServices

logger = logging.getLogger(__name__)

async def on_startup(
    bot: Bot, 
    chat_service: ChatService,
    user_service: UserServices
) -> None:
    """
    Функція, яка виконується при запуску бота.
    Встановлює вебхук.
    """
    
    logger.info("Bot is starting up...")
    
    os.makedirs(os.path.dirname(settings.SG_DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(settings.CHAT_DB_PATH), exist_ok=True)
    
    # 1. Встановлюємо з'єднання з БД
    await chat_service.connect()
    await user_service.connect()
    # 2. Ініціалізуємо таблиці
    
    await chat_service.initialize_db()
    await user_service.initialize_db()
    
    # 3. Встановлюємо вебхук (якщо використовується)
    # await bot.set_webhook(...) 
    logger.info("Bot has started successfully.")

async def on_shutdown(
    bot: Bot, 
    chat_service: ChatService,
    user_service: UserServices
) -> None:
    """
    Функція, яка виконується при зупинці бота.
    Видаляє вебхук.
    """
    logger.warning("Bot is shutting down...")
    await chat_service.close()
    await user_service.close()
    