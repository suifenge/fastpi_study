import aioredis
from aioredis import Redis

from config import *


def get_redis() -> Redis:
    redis = aioredis.from_url(url=REDIS_URI, decode_responses=True)
    return redis
