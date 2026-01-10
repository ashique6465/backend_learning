from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from sqlalchemy.orm import Session

from .database import get_db 
from .jwt import decode_token
from .crud import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = decode_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Invalid token"
            )
    except JWTError:
        raise HTTPException(
            status_code=401, detail="Invalid token"
        )
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=401, detail= "User not found"
        )
    return user