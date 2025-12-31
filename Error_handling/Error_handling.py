#Bad Request(400):- Request is syntactically correct but logically wrong
#Ex - Password and confirm password don't match

from fastapi import HTTPException

if password != confirm_password:
    raise HTTPException(
        status_code=400,
        detail="Password do not match"
    )


#Unauthorized(401):- User is not authentication, Missing or invalid token

raise HTTPException(
    status_code=401,
    detail="Invalid or expired token"
)


#Forbidden(403):- User is authenticated but not allowed

if user.role != "admin":
    raise HTTPException(
        status_code="403",
        detail="You don't have permission"
    )


#Not Found(404):- Resource doesn't exist

user = db.get_user(user_id)
if not user:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


#conflict(409):- Data already exists but voiletes uniqueness

if db.email_exists(email):
    raise HTTPException(
        status_code=409,
        detail="Email already registered"
    )


#Server Error-Our fault(backend issue)

#Internal Server Error(500):- Unexpected crash, bug in code, unhandled exception

try:
    risk_operation()
except Exception:
    raise HTTPException(
        status_code=500,
        detail="Something went wrong"
    )

#Service Unavailable(503):-Dependency is down, DB, Redis, external API

raise HTTPException(
    status_code=503,
    detail="Service temporarily unavailable"
)

#Gateway Timeout(504):- External service took too long

raise HTTPException(
    status_code=504,
    detail="Upstream service timeout"
)


#Business logic error
#1.Cannot cancel shipped order
#2.Insufficient balance
#3.Booking already confirmed

if order.status == "SHIPPPED":
    raise HTTPException(
        status_code=400,
        detail="Cannot cancel shipped order"
    )


#Authentication and Authorization error
#Token error
#Missing token - 401
#Invalid token - 401
#Expired token - 401
#Insufficient role - 403



#Database Errors
#Record not found
if not record:
    raise HTTPException(404,"Record not found")

#constraint violations
except IntegrityError:
    raise HTTPException(409, "Duplicate record")


#Database connection failure
except DBConnectionError:
    raise HTTPException(503, "Database unavailable")
