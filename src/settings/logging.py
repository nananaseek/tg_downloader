import logging.config
import os
import sys

# Зчитуємо режим роботи зі змінних оточення.
# 'deploy' - це безпечне значення за замовчуванням.
LOGGING_MODE = os.getenv("LOGGING_MODE", "deploy")

# --- Словник конфігурації ---

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False, # Важливо, щоб не вимкнути логери бібліотек

    # --- Форматери: визначають вигляд лог-повідомлень ---
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - [%(filename)s:%(lineno)d] - %(message)s"
        },
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        },
    },

    # --- Хендлери: визначають, куди відправляти логи (консоль, файл) ---
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose", # Детальний формат для консолі
            "stream": sys.stdout,
        },
        "info_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default", # Стандартний формат для файлу
            "filename": "logs/info.log",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 10,
            "encoding": "utf8",
        },
        "error_file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "formatter": "verbose", # Детальний формат для помилок
            "filename": "logs/errors.log",
            "maxBytes": 10485760,  # 10 MB
            "backupCount": 10,
            "encoding": "utf8",
        },
    },

    # --- Логери: зв'язують все разом ---
    "loggers": {
        "aiogram": { # Логер для самої бібліотеки aiogram
            "level": "WARNING" if LOGGING_MODE == "deploy" else "INFO",
            "handlers": ["console"] if LOGGING_MODE == "debug" else ["info_file_handler", "error_file_handler"],
            "propagate": False, # Щоб повідомлення не дублювалися у root логері
        },
        "bot_app": { # Спеціальний логер для нашого застосунку
            "level": "INFO" if LOGGING_MODE == "deploy" else "DEBUG",
            "handlers": ["console"] if LOGGING_MODE == "debug" else ["info_file_handler", "error_file_handler"],
            "propagate": False,
        }
    },
    
    # --- Root логер: ловить все, що не оброблено іншими логерами ---
    "root": {
        "level": "INFO" if LOGGING_MODE == "deploy" else "DEBUG",
        "handlers": ["console"] if LOGGING_MODE == "debug" else ["info_file_handler", "error_file_handler"],
    },
}

def setup_logging():
    """Застосовує конфігурацію логування."""
    # Створюємо папку для логів, якщо її не існує
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("bot_app")
    logger.info(f"Logging configured for '{LOGGING_MODE}' mode.")