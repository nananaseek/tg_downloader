import os
import asyncio
import requests
import logging

from TikTokApi import TikTokApi

from src.settings.config import settings


logger = logging.getLogger(__name__)


async def get_video_from_tiktok(url: str, raw_file: bool = False, num_sessions: int = 3):
    async with TikTokApi() as api:
        await api.create_sessions(
            ms_tokens=[settings.TT_TOKEN], 
            num_sessions=num_sessions, 
            sleep_after=3, 
            browser=os.getenv("TIKTOK_BROWSER", "chromium")
        )
        
        video = api.video(
            url=url
        )
        
        logger.debug("Download video info")
        await video.info()
        
        logger.debug("Get session")

        _, session = api._get_session()

        logger.debug("Get session cookies")
        cookies = await api.get_session_cookies(session)

        
        playAddr = video.as_dict["video"]["playAddr"]
        
        h = session.headers
        h["range"] = 'bytes=0-'
        h["accept-encoding"] = 'identity;q=1, *;q=0'
        h["referer"] = 'https://www.tiktok.com/'

        logger.debug("Get video content")       
        resp = requests.get(playAddr, headers=h, cookies=cookies)
        
        if raw_file:
            logger.debug("Send video to client")
            description = video.as_dict["desc"]
            
            text = f"{description}"
            return resp.content, text
            # return await video.bytes(), text
        else:
            os.makedirs("tiktok_downloads", exist_ok=True)
            logger.debug("Save video")
            with open("tiktok_downloads/video.mp4", "wb") as f:
                f.write(resp.content)
        




if __name__ == "__main__":
    url = "https://vm.tiktok.com/ZMSX63A5F/"
    
    asyncio.run(get_video_from_tiktok(url))