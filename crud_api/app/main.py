from fastapi import FastAPI, Depends
# from fastapi import HTTPException
# from sqlalchemy.orm import Session

from .database import Base, engine
from . import models
# from .database import get_db
# from . import models, schemas, crud 
from .auth import router as auth_router
from . dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app =FastAPI()
app.include_router(auth_router)

#protected route 
@app.get("/protected")
def protected_route(current_user=Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": current_user.id,
        "email": current_user.email
    }

# @app.post("/users/", response_model=schemas.UserResponse)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     return crud.create_user(db, user)


# @app.get("/users/", response_model=list[schemas.UserResponse])
# def read_users(db:Session = Depends(get_db)):
#     return crud.get_users(db)


# @app.get("/users/{user_id}", response_model=schemas.UserResponse)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = crud.get_user(db, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail = "User not found")
#     return user 

# @app.put("/users/{user_id}", response_model=schemas.UserResponse)
# def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     updated_user = crud.update_user(db, user_id, user)
#     if not updated_user:
#         raise HTTPException(status_code=404, detail= "Use not found")
#     return updated_user

# @app.delete("/users/{user_id}")
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     deleted = crud.delete_user(db, user_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="User not found")
#     return {"message": "User deleted "}

