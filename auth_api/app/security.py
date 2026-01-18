from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime, timedelta


SECRET_KEY = "secret"
ALGORITHM = "HS256"
TOKEN_BLACKLIST = set()

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str):
    password = password[:72]
    return pwd_context.hash(password)



def verify_password(password: str , hashed: str):
    password = password[:72]
    return pwd_context.verify(password,hashed)


def create_access_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=30)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def blacklist_token(token: str):
    TOKEN_BLACKLIST.add(token)

def is_token_blacklisted(token:str) -> bool:
    return token in TOKEN_BLACKLIST
