import logging
import asyncio

from src.core import start_bot
from src.settings.logging import setup_logging

def main():
    setup_logging()
    
    try:
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")