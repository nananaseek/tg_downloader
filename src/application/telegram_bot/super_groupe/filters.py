from aiogram.filters import Filter
from aiogram.types import Message

from src.application.telegram_bot.super_groupe.services import ChatService

class ChatActiveFilter(Filter):
    async def __call__(self, message: Message, chat_service: ChatService) -> bool:
        if message.is_topic_message:
            return await chat_service.is_chat_active(message.message_thread_id)
        else:
            return None
