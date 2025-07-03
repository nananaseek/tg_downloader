import os
import asyncio
import logging
from aiogram import F, Router, types, Bot
from aiogram.enums import MessageEntityType

from utils import check_for_files_in_directory
from src.application.instadowloader import InstagramDownloader
from src.application.tiktok_down import get_video_from_tiktok

from src.application.telegram_bot.super_groupe.services import ChatService
from src.application.telegram_bot.super_groupe.filters import ChatActiveFilter
from src.application.telegram_bot.super_groupe.utils import (
    classify_social_media_url,
    instagram_video_url
)

from src.application.tiktok_down.utils import count_files_in_project_tmp_dir, create_kostil


logger = logging.getLogger(__name__)


monitoring_router = Router()
monitoring_router.message.filter(ChatActiveFilter())


@monitoring_router.message(F.entities.func(lambda entities: any(entity.type == MessageEntityType.URL for entity in entities)))
async def handle_links(message: types.Message, bot: Bot, chat_service: ChatService):
    for entity in message.entities:
        if entity.type == MessageEntityType.URL:
                        
            message_text = message.text
            classify_url = classify_social_media_url(message_text)
            
            if classify_url.get("inst"):
            
                while check_for_files_in_directory("reels_downloads"):
                    await asyncio.sleep(1)
                
                Inst = InstagramDownloader(url=message_text,)
                is_download = Inst.download_media_by_url()
                
                if is_download:
                    video_data, text = instagram_video_url()
                    
                    video = types.BufferedInputFile(
                        file=video_data,
                        filename="video.mp4"
                    )
                    
                    await message.reply_video(video=video, caption=text)
                    
                else:
                    await message.reply("Помилка в завантаженні відео, надсилаю посилання в чат з помилками для ручного завантаження")
                    thread_id = message.message_thread_id
                    chat_id = message.chat.id
                    error_chat_id = await chat_service.get_error_chat(thread_id)
                    if error_chat_id:
                        await bot.send_message(
                            chat_id=chat_id, 
                            message_thread_id=error_chat_id,
                            text=message_text
                        )
                    else:
                        await message.answer("Чат для відео з помилками не знайдений.")
                        
            elif classify_url.get("tt"):
                while count_files_in_project_tmp_dir() >= 2:
                    await asyncio.sleep(1)
                
                logger.info(f"Downloading TikTok video from {message_text}")
                kostyl = create_kostil()
                
                video_data, text = await get_video_from_tiktok(
                    url=message_text,
                    raw_file=True
                )
                
                video = types.BufferedInputFile(
                    file=video_data,
                    filename="video.mp4"
                )
                
                await message.reply_video(video=video, caption=text)
                
                os.remove(kostyl)
                
        else:
            pass