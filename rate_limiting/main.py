from fastapi import FastAPI, Request, Depends
from rate_limiter import rate_limiter


app = FastAPI(title="Redis Rate Limited API")


@app.get("/")
def home(
    request: Request,
    _: None = Depends(rate_limiter)
):
    return {"message": "Request allowed"}