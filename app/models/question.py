from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Question(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    topic_id: int = Field(
        foreign_key="topic.id",
        index=True
    )

    level: str

    question: str

    option_a: str

    option_b: str

    option_c: str

    option_d: str

    correct_answer: str = Field(
        max_length=1
    )

    explanation: str | None = None

    source: str = Field(
        default="manual"
    )

    created_by: int = Field(
        foreign_key="user.id"
    )

    is_active: bool = Field(
        default=True
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )