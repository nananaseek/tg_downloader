from aiogram import Router
from aiogram.filters import Command

from .help import help_command

command_router = Router()

command_router.message.register(
    help_command,
    Command("help")
)