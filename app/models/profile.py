from typing import Optional

from sqlmodel import SQLModel, Field


class Profile(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="user.id",
        unique=True
    )

    full_name: Optional[str] = None

    headline: Optional[str] = None

    bio: Optional[str] = None

    city: Optional[str] = None

    country: Optional[str] = None

    college: Optional[str] = None

    profile_picture: Optional[str] = None

    github_url: Optional[str] = None

    linkedin_url: Optional[str] = None

    website_url: Optional[str] = None

    rating: float = 0

    total_sessions: int = 0

    total_tokens_earned: int = 0