from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt


from .schemas import UserCreate
from .security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM

router = APIRouter()

fake_db = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@router.post("/register")
def register(user: UserCreate):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="User exists")
    fake_db[user.email] = hash_password(user.password)
    return {"message": "registered"}


@router.post("/login")
def login(user: UserCreate):
    hashed = fake_db.get(user.email)
    if not hashed or not verify_password(user.password,hashed):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
    return payload["sub"]

@router.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"message": f"hello {user}"}