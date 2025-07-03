from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from ...servises import UserServices


start_router = Router()

@start_router.message(CommandStart())
async def start_command(message: Message, user_service: UserServices):
    await user_service.register_user(
        user_id=int(message.from_user.id),
        username=str(message.from_user.username)
    )

    await message.answer("Привіт я робот для скачування відео з Instagram та TikTok (відео з тт будуть без водяних знаків)")
