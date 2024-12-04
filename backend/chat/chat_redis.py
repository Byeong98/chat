import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from decouple import config

redis_pool = ConnectionPool(host = config("REDIS_ADDRESS"),
                                port= config("REDIS_PORT"),
                                password=config("REDIS_PASSWORD"), 
                                db=0,
                                max_connections=10
                                )
redis_client = redis.Redis(connection_pool=redis_pool)

async def add_user_to_redis(key: str, value: str):
    await redis_client.sadd(key, value)

async def remove_user_to_redis(key: str, value: str):
    await redis_client.srem(key, value)

async def get_users_from_redis(key: str):
    users = await redis_client.smembers(key)
    return users