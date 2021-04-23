import redis
from config import *

r = redis.StrictRedis(
    host=host_redis,  # из Endpoint
    port=12573,  # из Endpoint
    password=password_redis,
    decode_responses=True,
    charset="utf-8")
