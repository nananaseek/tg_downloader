from playwright.async_api import async_playwright
from TikTokApi.helpers import random_choice

# from TikTokApi import TikTokApi

# class ModifyTikTokAPI(TikTokApi):

class PlayWright:
    playwright = None
    browser = None
    
    async def run_instans(self):
        self.playwright = await async_playwright().start()
        override_browser_args = ["--headless=new"]
        headless = False 
        self.browser = await self.playwright.chromium.launch(
            headless=headless, args=override_browser_args, proxy=random_choice(None), executable_path=None
        )

    async def stop_playwright(self):
        """Stop the playwright browser"""
        if self.browser or self.playwright:
            return
        await self.browser.close()
        await self.playwright.stop()
        
play_wright = PlayWright()