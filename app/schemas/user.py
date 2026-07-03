from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class ResetPassword(BaseModel):
    token: str
    new_password: str