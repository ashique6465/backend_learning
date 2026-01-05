from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta



app = FastAPI()
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

fake_user_db = {
    "user@gmail.com":{
        "id":101,
        "email": "user@gmail.com",
        "hashed_password": "123456",
        "role": "admin"
    }
}

def create_access_token(data:dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)


@app.post("/login")
def login(email: str, password: str):
    user = fake_user_db.get(email)

    if not user or password != user["hashed_password"]:
        raise HTTPException(status_code = 401, detail = "Invalid credential")

        token = create_access_token(
            data={"sub": user["email"], "role": user["role"]},
            expires_delta=timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": token, "token_type": "bearer"}