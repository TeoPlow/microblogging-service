import redis.asyncio as redis
from app.config import Config


def get_redis_client():
    """
    Функция для создания и возврата асинхронного клиента Redis.
    """
    return redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        db=0,
        decode_responses=True
    )
