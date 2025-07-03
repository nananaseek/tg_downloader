import logging

from typing import Optional

from src.settings.config import settings
from src.core.database import MainDBService

logger = logging.getLogger(__name__)

class ChatService(MainDBService):
    db_path = settings.SG_DB_PATH

    async def initialize_db(self) -> None:
        """
        Ініціалізує таблицю, використовуючи існуюче з'єднання.
        """
        db = await self._get_connection()
        await db.execute("""
            CREATE TABLE IF NOT EXISTS active_chats (
                message_thread_id INTEGER PRIMARY KEY,
                name VARCHAR(32),
                error_chat INTEGER NULL
            );
        """)
        await db.commit()
        logger.info("Database for ChatService has been initialized.")

    async def add_chat(self, message_thread_id: int, name: str) -> None:
        """Додає чат, використовуючи існуюче з'єднання."""
        try:
            db = await self._get_connection()
            await db.execute(
                "INSERT OR IGNORE INTO active_chats (message_thread_id, name) VALUES (?, ?)",
                (message_thread_id, name),
            )
            await db.commit()
            logger.info(f"Chat {message_thread_id} with name '{name}' added to active list in DB.")
        except Exception as e:
            logger.error(f"Failed to add chat {message_thread_id}: {e}")
    
    async def add_error_chat(self, name: str, error_chat_id: int) -> None:
        """
        Встановлює ID чату для помилок для запису, знайденого за іменем.

        Args:
            name: Ім'я чату, який потрібно оновити.
            error_chat_id: ID чату для помилок.
        """
        try:
            db = await self._get_connection()
            cursor = await db.execute(
                "UPDATE active_chats SET error_chat = ? WHERE name = ?",
                (error_chat_id, name),
            )
            await db.commit()
            # Перевіряємо, чи був оновлений хоча б один рядок
            if cursor.rowcount > 0:
                logger.info(f"Successfully set error_chat for chat '{name}' to {error_chat_id}.")
            else:
                logger.warning(f"No chat found with name '{name}' to update error_chat.")
        except Exception as e:
            logger.error(f"Failed to update error_chat for chat '{name}': {e}")
                
    async def get_error_chat(self, message_thread_id: int) -> Optional[int]:
        """
        Отримує ID чату для помилок за іменем чату.

        Args:
            message_thread_id: Ім'я чату для пошуку.

        Returns:
            ID чату для помилок (int) або None, якщо чат не знайдено
            або поле error_chat не встановлено.
        """
        try:
            db = await self._get_connection()
            cursor = await db.execute(
                "SELECT error_chat FROM active_chats WHERE message_thread_id = ?",
                (message_thread_id,),
            )
            row = await cursor.fetchone()
            if row:
                logger.debug(f"Found error_chat ID {row[0]} for chat message_thread_id '{message_thread_id}'.")
                return row[0]
            else:
                logger.info(f"No chat found with message_thread_id '{message_thread_id}' when getting error_chat.")
                return None
        except Exception as e:
            logger.error(f"Failed to get error_chat for message_thread_id '{message_thread_id}': {e}")
            return None

    async def is_chat_active(self, message_thread_id: int) -> bool:
        """Перевіряє чат, використовуючи існуюче з'єднання."""
        db = await self._get_connection()
        cursor = await db.execute("SELECT 1 FROM active_chats WHERE message_thread_id = ? LIMIT 1", (message_thread_id,))
        result = await cursor.fetchone()
        return result is not None
    
    async def is_chat_error(self, message_thread_id: int) -> bool:
        """Перевіряє чат, використовуючи існуюче з'єднання."""
        db = await self._get_connection()
        cursor = await db.execute("SELECT 1 FROM active_chats WHERE error_chat = ? LIMIT 1", (message_thread_id,))
        result = await cursor.fetchone()
        return result is not None
    
    async def get_branch_name(
        self, 
        message_thread_id: int | None = None, 
        error_chat: int | None = None
    ) -> str:
        """Повертає назву гілки для чату, використовуючи існуюче з'єднання."""
        db = await self._get_connection()
        if message_thread_id:
            cursor = await db.execute("SELECT name FROM active_chats WHERE message_thread_id = ?", (message_thread_id,))
        elif error_chat:
            cursor = await db.execute("SELECT name FROM active_chats WHERE error_chat = ?", (error_chat,))
        elif (error_chat is None) and (message_thread_id is None):
            return None
        result = await cursor.fetchone()
        return result[0] if result else None
    
    async def remove_chat(self, message_thread_id: int) -> None:
        """Видаляє чат, використовуючи існуюче з'єднання."""
        db = await self._get_connection()
        await db.execute("DELETE FROM active_chats WHERE message_thread_id = ?", (message_thread_id,))
        await db.commit()
        logger.info(f"Chat {message_thread_id} removed from active list in DB.")