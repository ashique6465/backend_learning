import json
from redis_client import redis_client


PRODUCTS_CACHE_KEY = "products:list:v1"
CACHE_TTL = 60 

def get_products_cache():
    cached_data = redis_client.get(PRODUCTS_CACHE_KEY)

    if cached_data:
        print("REDIS CACHE HIT")
        return json.loads(cached_data)

    print("REDIS CACHE MISS")
    return None

def set_products_cache(products: list):
    redis_client.setex(
        PRODUCTS_CACHE_KEY,
        CACHE_TTL,
        json.dumps(products)
    )

def invalidate_products_cache():
    redis_client.delete(PRODUCTS_CACHE_KEY)