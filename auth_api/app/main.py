from fastapi import FastAPI 
from app.auth import router


app = FastAPI()
app.include_router(router)