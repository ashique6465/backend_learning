print("🔥 rate_limiter.py LOADED 🔥")
from fastapi import Request, HTTPException
from redis_client import redis_client

RATE_LIMIT = 5 
WINDOW_SIZE = 30


def rate_limiter(request: Request):
    print("RATE LIMITER CALLED")

    client_ip = request.client.host

    redis_key = f"rate_limit:{client_ip}"
    print("Redis key:", redis_key)

    current_count = redis_client.incr(redis_key)
    print("Current count:", current_count)

    if current_count == 1 :
        redis_client.expire(redis_key, WINDOW_SIZE)


    if current_count > RATE_LIMIT:
        raise HTTPException(
            status_code = 429,
            detail = "Too many requests"
        )