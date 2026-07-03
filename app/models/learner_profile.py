from typing import Optional

from sqlmodel import SQLModel, Field


class LearnerProfile(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="user.id",
        unique=True
    )

    learning_goal: Optional[str] = None

    preferred_language: Optional[str] = None

    education_level: Optional[str] = None

    current_level: Optional[str] = None