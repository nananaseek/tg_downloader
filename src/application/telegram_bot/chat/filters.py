from aiogram.filters import Filter
from aiogram.types import Message

class PrivateFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        return False if message.is_topic_message else True
