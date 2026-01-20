import json
import time 
from fastapi import Request
from redis_client import redis_client

CACHE_TTL = 30 #Seconds

def get_cache(request: Request):
    cache_key = f"cache:{request.url}"

    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("CACHE HIT")
        return json.loads(cached_data)

    print("CACHE MISS")
    return None

def set_cache(request: Request, response: dict):
    cache_key = f"cache:{request.url}"

    redis_client.setex(
        cache_key,
        CACHE_TTL,
        json.dumps(response)
    )