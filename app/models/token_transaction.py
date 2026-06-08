from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TokenTransaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    sender_id: int = Field(foreign_key="user.id")
    receiver_id: int = Field(foreign_key="user.id")

    amount: int
    session_id: int = Field(foreign_key="session.id")

    created_at: datetime = Field(default_factory=datetime.utcnow)