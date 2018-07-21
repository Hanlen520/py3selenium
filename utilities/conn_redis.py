import redis, settings


def redis_connect(host=settings.CACHED_REDIS_HOST, port=settings.CACHED_REDIS_PORT):
    # Connect to the redis
    redis_client = redis.StrictRedis(host=host, port=port)
    return redis_client