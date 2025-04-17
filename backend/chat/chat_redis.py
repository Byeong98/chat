import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from decouple import config

redis_pool = ConnectionPool(host = config("REDIS_ADDRESS"),
                                port= config("REDIS_PORT"),
                                password=config("REDIS_PASSWORD"), 
                                db=0,
                                max_connections=100
                                )
redis_client = redis.Redis(connection_pool=redis_pool)

#접속자 추가, ranking 접속자 증가
async def add_user_to_redis(key: str, value: str):
    await redis_client.sadd(key, value)
    await redis_client.zincrby('chatroom_ranking', 1, key)

#접속자 삭제, rnaking 접속자 감소
async def remove_user_to_redis(key: str, value: str):
    await redis_client.srem(key, value)
    current_users_count = await redis_client.zincrby('chatroom_ranking', -1, key)
    
    if int(current_users_count) <= 0:
        await redis_client.zrem('chatroom_ranking', key)
        return True

#모든 접속자 조회
async def get_users_from_redis(key: str):
    users = await redis_client.smembers(key)
    return users

#모든 채팅방 접속자 가져오기 
async def get_list_from_redis():
    return await redis_client.zrevrange('chatroom_ranking',0,-1, withscores=True)

async def remove_user_and_get_users_from_redis(key: str, value: str):
    # 접속자 제거
    await redis_client.srem(key, value)

    # 최신 접속자 목록 반환
    # users = await redis_client.smembers(key)

    # return users