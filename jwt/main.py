from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str

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

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")
        role: str = payload.get("role")

        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return {
            "email": email,
            "role": role
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid or expired"
        )
@app.post("/login")
def login(data: LoginRequest):
    user = fake_user_db.get(data.email)

    if not user or data.password != user["hashed_password"]:
        raise HTTPException(status_code=401, detail="Invalid credential")

    token = create_access_token(
        data={"sub": user["email"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user