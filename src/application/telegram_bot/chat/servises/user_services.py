import logging

from src.core.database import MainDBService
from src.settings.config import settings


logger = logging.getLogger(__name__)

class UserServices(MainDBService):
    db_path = settings.CHAT_DB_PATH
    
    async def initialize_db(self) -> None:
        """
        Ініціалізує таблицю, використовуючи існуюче з'єднання.
        """
        db = await self._get_connection()
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username VARCHAR(64)
            );
        """)
        await db.commit()
        logger.info("Database for UserService has been initialized.")
    
    async def register_user(self, user_id: int, username: str) -> None:
        try:
            db = await self._get_connection()
            await db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username,))
            await db.commit()
            cursor = await db.execute("SELECT changes()",)
            if (await cursor.fetchone())[0] > 0:
                logger.info(f"User {user_id} registered.")
            else:
                logger.info(f"User {user_id} already existed (ignored insertion).")
        except Exception as e:
            logger.error(f"Error registering user: {e}", exc_info=True)
            
    async def is_user_registered(self, user_id: int) -> bool:
        """Перевіряє чи зареєстрований користувач"""
        db = await self._get_connection()
        cursor = await db.execute("SELECT 1 FROM users WHERE user_id = ? LIMIT 1", (user_id,))
        result = await cursor.fetchone()
        return result is not None

    async def get_user_username(self, user_id: int) -> str:
        """Повертає ім'я користувача"""
        db = await self._get_connection()
        cursor = await db.execute("SELECT username FROM users WHERE user_id = ? LIMIT 1", (user_id,))
        result = await cursor.fetchone()
        return result[0] if result else None
