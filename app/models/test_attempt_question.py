from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class TestAttemptQuestion(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    attempt_id: int = Field(
        foreign_key="testattempt.id",
        index=True
    )

    question_id: int = Field(
        foreign_key="question.id",
        index=True
    )

    question_order: int

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )