from datetime import datetime, timedelta
from jose import JWTError,  jwt 

SECRET_KEY = "your_secret_key"
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#create access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

#decode access token
def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])