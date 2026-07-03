from typing import Optional

from sqlmodel import SQLModel, Field


class TutorProfile(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="user.id",
        unique=True
    )

    experience_years: Optional[int] = None

    education: Optional[str] = None

    teaching_style: Optional[str] = None

    languages: Optional[str] = None

    hourly_tokens: int = 10

    intro_video_url: Optional[str] = None

    resume_url: Optional[str] = None