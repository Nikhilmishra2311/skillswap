from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class TestAttempt(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", index=True)

    user_skill_id: int = Field(foreign_key="userskill.id", index=True)

    topic_id: int = Field(foreign_key="topic.id", index=True)

    total_questions: int = 10

    correct_answers: int = 0

    percentage: float = 0

    passed: bool = False

    is_completed: bool = False

    started_at: datetime = Field(default_factory=datetime.utcnow)

    submitted_at: Optional[datetime] = None

    expires_at: datetime

    created_at: datetime = Field(default_factory=datetime.utcnow)