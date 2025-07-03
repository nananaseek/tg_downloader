import logging
from aiogram import Router, F, Bot, types
from aiogram.enums import MessageEntityType
from aiogram.filters import Command

from src.application.telegram_bot.super_groupe.services import ChatService

logger = logging.getLogger(__name__)

activation_router = Router()


@activation_router.message(
    F.text, 
    F.is_topic_message,
    F.entities.func(
        lambda entities: any(
            entity.type == MessageEntityType.MENTION for entity in entities
        )
    )
)
async def handle_bot_mention(message: types.Message, bot: Bot, chat_service: ChatService):
    text = message.text.split(" ")
    if len(text) == 2:
        name = text[-1]
        me = await bot.get_me()
        logger.debug(f"Message entities: {message.entities}")
        mentioned_bots = [
            entity for entity in message.entities 
            if entity.type == MessageEntityType.MENTION
        ]
    elif (len(text) == 3) and (text[-1] == "error"):
        name = text[1]
        mentioned_bots = []
        await chat_service.add_error_chat(name, message.message_thread_id)
        await message.answer("Гілку прикріплено як для посилань з помилками")
    else:
        mentioned_bots = []
        await message.answer("Не вказана назва чату!")
    
    for entity in mentioned_bots:
        mentioned_text = message.text[entity.offset : entity.offset + entity.length]
        if mentioned_text == f"@{me.username}":
            
            if not await chat_service.is_chat_active(message.message_thread_id):
                                
                await chat_service.add_chat(message.message_thread_id, name)
                await message.reply(
                    "Дякую! Тепер я буду моніторити посилання у чаті."
                )
            else:
                await message.reply("Я вже моніторю цей чат.")
            break

@activation_router.message(F.is_topic_message, Command("status"))
async def check_status(message: types.Message, chat_service: ChatService):
    if await chat_service.is_chat_active(message.message_thread_id):
        branch_name = await chat_service.get_branch_name(
            message_thread_id=message.message_thread_id
        )
        await message.answer(f"✅ Моніторинг у цьому чаті активний ({branch_name}).")
    elif await chat_service.is_chat_error(message.message_thread_id):
        branch_name = await chat_service.get_branch_name(
            error_chat=message.message_thread_id
        )
        await message.answer(f"Чат для виводу помилок з гілки {branch_name}")
    else:
        await message.answer("❌ Моніторинг у цьому чаті неактивний. Згадайте мене (@bot_username), щоб активувати.")