from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TestAttempt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    topic_id: int = Field(foreign_key="topic.id")

    level: str   # 🔥 add this (important)

    score: int
    total: int

    passed: bool = False

    created_at: datetime = Field(default_factory=datetime.utcnow)  # 🔥 add this