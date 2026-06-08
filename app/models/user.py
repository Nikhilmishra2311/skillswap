from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    token_balance: int = 100   # default starting tokens
    email: str = Field(index=True, unique=True)
    password: str
    bio: str | None = None
    token_balance: int = 100
    is_deleted: bool = False