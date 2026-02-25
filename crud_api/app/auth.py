from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import schemas, crud 
from .jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

#register route
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


#login route
@router.post("/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticate_user = crud.authenticate_user(
        db, user.email, user.password
    )
    if not authenticate_user:
        raise HTTPException(
            status_code=401, detail="Invalid credentials"
        )
    token = create_access_token(
        data={"sub": str(authenticate_user.id)}
    )

    return {"access_token": token, "token_type": "bearer"}