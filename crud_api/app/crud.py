from sqlalchemy.orm import Session
from . import models, schemas
from .security import hash_password, verify_password

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None
    return user

#get User
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# def get_users(db: Session):
#     return db.query(models.User).all()


# def get_user(db:Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()



# def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         return None
#     db_user.name = user.name 
#     db_user.email = user.email

#     db.commit()
#     return db_user

# def delete_user(db: Session, user_id: int):
#     db_user = get_user(db, user_id)
#     if not db_user:
#         return None
#     db.delete(db_user)
#     db.commit()
#     return db_user