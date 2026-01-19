from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt


from .schemas import UserCreate
from .security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from app.security import is_token_blacklisted
from app.security import blacklist_token

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
    refresh_token = create_refresh_token()
    ReFRESH_TOKENS[refresh_token] = user.email
    return {
        "access_token": token,
        "refresh_token": refresh_token
    
    }

@router.post("/refresh")
def refresh_token(refresh_token: str):
    email = ReFRESH_TOKENS.get(refresh_token)
    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
        new_access_token = create_access_token({"sub": email})
        return {"access_token": new_access_token}

@router.post("/logout")
def logout(refresh_token: str):
    ReFRESH_TOKENS.pop(refresh_token, None)
    return {"message": "Logged out successfully"}
def get_current_user(token: str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token revoked")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload["sub"]



@router.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"message": f"hello {user}"}