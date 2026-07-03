from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    full_name: str
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    password: str
    bio: str | None = None
    token_balance: int = Field(default=100)
    
    role: str = "user"
    is_deleted: bool = False