import redis

from config import config

r_client = redis.asyncio.Redis(
    host=config["redis"]["host"],
    port=config["redis"]["port"]
)
