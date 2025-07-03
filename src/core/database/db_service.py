import aiosqlite
import logging

from typing import Optional


logger = logging.getLogger(__name__)

class MainDBService:
    db_path: str = ""
    _connection: Optional[aiosqlite.Connection] = None
    
    async def connect(self) -> None:
        """
        Встановлює постійне з'єднання з базою даних.
        Викликається один раз при старті бота.
        """
        if self._connection is None:
            self._connection = await aiosqlite.connect(self.db_path)
            logger.info("Database connection established.")

    async def close(self) -> None:
        """
        Закриває з'єднання з базою даних.
        Викликається один раз при зупинці бота.
        """
        if self._connection:
            await self._connection.close()
            self._connection = None
            logger.info("Database connection closed.")

    async def _get_connection(self) -> aiosqlite.Connection:
        """Внутрішній метод для отримання активного з'єднання."""
        if self._connection is None:
            # Це аварійна ситуація, з'єднання має бути встановлено на старті
            raise RuntimeError("Database connection is not established. Call connect() first.")
        return self._connection
