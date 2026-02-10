from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt


from .schemas import UserCreate
from .security import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from app.security import is_token_blacklisted
from app.security import blacklist_token
from app.security import ROLE_PERMISSIONS


router = APIRouter()

fake_db = {}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#register
@router.post("/register")
def register(user: UserCreate):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="User exists")
    fake_db[user.email] = {
        "password":
        hash_password(user.password),
        "role": user.role
        }
    return {"message": "registered"}

#login
@router.post("/login")
def login(user: UserCreate):
    user_record = fake_db.get(user.email)
    if not user_record or not verify_password(user.password, user_record["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    

    permissions = ROLE_PERMISSIONS.get(user_record["role"], [])
    token = create_access_token({
        "sub": user.email,
        "role": user_record["role"],
        "permissions": permissions
    })
    refresh_token = create_refresh_token()
    ReFRESH_TOKENS[refresh_token] = user.email
    return {
        "access_token": token,
        "refresh_token": refresh_token
    
    }


#refresh token
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
#logout
@router.post("/logout")
def logout(refresh_token: str):
    ReFRESH_TOKENS.pop(refresh_token, None)
    return {"message": "Logged out successfully"}

#get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token revoked")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return {
        "email": payload["sub"],
        "role": payload["role"],
        "permissions": payload.get("permissions", [])
    }
#permission and role checks
def require_permission(required_permission: str):
    def checker(user=Depends(get_current_user)):
        if required_permission not in user["permissions"]:
            raise HTTPException(
                status_code=403,
                detail="Permission denied"
            )
        return user 
    return checker

def require_role(require_role: str):
    def checker(user=Depends(get_current_user)):
        if user["role"] != require_role:
            raise HTTPException(status_code=403,detail="Forbidden")
        return user
    return checker


@router.get("/admin")
def admin_only(user=Depends(require_role("admin"))):
    return {"message": f"Welcome admin {user['email']}"}

@router.get("/admin/users")
def list_users(
    user = Depends(require_permission("user:read"))
):

    return fake_db


@router.delete("/admin/users/{email}")
def delete_user(
    email: str , 
    user = Depends(require_permission("user:delete"))
):
    fake_db.pop(email, None)
    return {"message": "Deleted"}
@router.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"message": f"hello {user}"}