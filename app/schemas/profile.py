from typing import Optional

from pydantic import BaseModel


# -----------------------------
# Common Profile Update
# -----------------------------

class ProfileUpdate(BaseModel):

    full_name: Optional[str] = None

    headline: Optional[str] = None

    bio: Optional[str] = None

    city: Optional[str] = None

    country: Optional[str] = None

    college: Optional[str] = None

    github_url: Optional[str] = None

    linkedin_url: Optional[str] = None

    website_url: Optional[str] = None


# -----------------------------
# Public Profile Response
# -----------------------------

class ProfileResponse(BaseModel):

    user_id: int

    full_name: Optional[str]

    headline: Optional[str]

    bio: Optional[str]

    city: Optional[str]

    country: Optional[str]

    college: Optional[str]

    profile_picture: Optional[str]

    github_url: Optional[str]

    linkedin_url: Optional[str]

    website_url: Optional[str]

    rating: float

    total_sessions: int

    total_tokens_earned: int

    class Config:
        from_attributes = True