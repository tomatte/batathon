from chatbot.clients.redis_client import RedisClient 

_redis_client = None

def get_redis_client():
    global _redis_client
    if _redis_client is None:
        _redis_client = RedisClient("redis", 6379)
    return _redis_client
