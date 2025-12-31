from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict

app = FastAPI()

class AdvancedMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)

    async def log_message(self, message: str):
        print(message)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Rate limiting
        if current_time - self.rate_limit_records[client_ip] < 1:
            return Response(content="Rate limit exceeded", status_code=429)

        self.rate_limit_records[client_ip] = current_time

        path = request.url.path
        await self.log_message(f"Request to {path}")

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(process_time)

        await self.log_message(
            f"Response for {path} took {process_time:.4f} seconds"
        )

        return response

app.add_middleware(AdvancedMiddleware)

@app.get("/")
async def main():
    return {"message": "Hello, World"}


# from fastapi import FastAPI, Request
# import random
# import string
# app =FastAPI()

# @app.middleware("http")
# async def request_id_logging(request: Request, call_next):
#     response = await call_next(request)
#     random_letter = ''.join(random.choice(string.ascii_letters) for _ in range(10))
#     print(f"Log {random_letter}")
#     response.headers["X-Request-ID"] = random_letter
#     return response

# @app.get("/")
# async def say_hi():
#     return "Hello"
