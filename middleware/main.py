




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
