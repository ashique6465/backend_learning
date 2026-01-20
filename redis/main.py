from fastapi import FastAPI, Request, Depends
from rate_limiter import rate_limiter
from cache import get_cache, set_cache
import time

app = FastAPI(title="Redis Rate Limited & Cached API")


@app.get("/")
def home(
    request: Request,
    _: None = Depends(rate_limiter)
):
    return {"message": "Request allowed"}


@app.get("/data")
def get_data(
    request: Request,
    _: None = Depends(rate_limiter)
):
    cached = get_cache(request)
    if cached:
        return cached

    time.sleep(3)

    response = {
        "data": "Expensive data",
        "timestamp": time.time()
    }

    set_cache(request,response)
    return response