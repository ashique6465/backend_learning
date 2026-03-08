from fastapi import FastAPI, Response, Depends
from rate_limiter import rate_limiter
from db import get_all_products, add_product
from cache import (
    get_products_cache,
    set_products_cache,
    invalidate_products_cache
)

app = FastAPI(title="Redis Rate Limited & Cached API")

# The GET endpoint checks redis cache
@app.get("/products")
def get_products(
    response: Response,
    _: None = Depends(rate_limiter)
):

    #CDN
    response.headers["Cache-Control"] = "public, max-age=120"

    #Redis cache-aside
    cached = get_products_cache()
    if cached :
        return cached
    products = get_all_products()
    set_products_cache(products)
    return products

# The POST endpoint invalidates the cache after creating a new product
@app.post("/products")
def create_product(
    product: dict,
    _: None = Depends(rate_limiter)
):
    add_product(product)
    invalidate_products_cache()
    return {"status": "product created"}
