import os

from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv("API_KEY")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    TT_TOKEN = os.getenv("TT_TOKEN")
    
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    _DB_FOLDER = "database"
    SG_DB_PATH = f"{_DB_FOLDER}/main.db"
    CHAT_DB_PATH = f"{_DB_FOLDER}/chat.db"
    
    
    
settings = Settings()