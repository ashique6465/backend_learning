from pydantic import BaseModel,EmailStr, validator

class User(BaseModel):
    name: str 
    email: EmailStr 
    account: int 

    @validator("account")
    def validate_account_id(cls,value):
        if value <= 0 :
            raise ValueError(f"account must be positive: {value}")
        return value 

user = User(
    name = "ash",
    email = "ash@gmail.com",
    account = 1234
)

print(user)


