from aiogram.types import Message

async def help_command(message: Message):
    
    if message.is_topic_message:
        help_message = """Для того що б зареєструвати гілку надішліть таке повідомлення: `@botname {topic_name}`
        
    Для того що б зареєструвати гілку для виводу посилань які не обробилися пропишіть: `@botname {topic_name} error`
    """
    else:
        help_message = """Бот приймає посилання на відео в Instagram та TikTok і надсилає відео (ТТ відео без водяних знаків) """
    
    await message.answer(help_message)