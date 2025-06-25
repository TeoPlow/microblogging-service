import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Конфигурация приложения"""

    # Основные настройки
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URL = os.getenv(
        "SQLALCHEMY_DATABASE_URL",
        "postgresql+asyncpg://postgres:password@postgres:5432/service_db",
    )
    REDIS_HOST = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT = os.getenv("REDIS_PORT", "6379")

    # Настройка хранилища медиафайлов
    MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
    MINIO_ROOT_USER = os.getenv("MINIO_ROOT_USER", "user")
    MINIO_ROOT_PASSWORD = os.getenv("MINIO_ROOT_PASSWORD", "password")
    MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "media")

    # Настройки API (ничего не делает)
    API_VERSION = os.getenv("API_VERSION", "v1")
    API_KEY = os.getenv("API_KEY")

    # Настройки логирования
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_SAVE_TO_FILE = os.getenv("LOG_SAVE_TO_FILE", "False").lower() in [
        "true",
        "1",
    ]

    # Вывод всей конфигурации перед запуском приложения
    @classmethod
    def log_config(cls):
        from app.api.utils.logger import get_logger

        log = get_logger("ConfigLogger")

        log.debug(f"Текущий рабочий каталог: {os.getcwd()}")
        log.info("Текущая конфигурация:")
        for attr in dir(cls):
            if attr.isupper():
                value = getattr(cls, attr)

                if attr == "SQLALCHEMY_DATABASE_URL":
                    parsed = urlparse(value)
                    if parsed.username and parsed.password:
                        safe_value = value.replace(
                            f":{parsed.password}@", ":*****@"
                        )
                    else:
                        safe_value = value
                    log.info(f"{attr} = {safe_value}")

                elif attr in ["API_KEY", "MINIO_ROOT_PASSWORD"]:
                    safe_value = "*****"
                    log.info(f"{attr} = {safe_value}")

                else:
                    log.info(f"{attr} = {value}")
