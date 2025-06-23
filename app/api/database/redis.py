import redis.asyncio as redis
from app.config import Config


redis_client = redis.Redis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)
