from typing import Optional

from pydantic import BaseModel


# -----------------------------
# Create Tutor Profile
# -----------------------------

class TutorProfileCreate(BaseModel):

    experience_years: Optional[int] = None

    education: Optional[str] = None

    teaching_style: Optional[str] = None

    languages: Optional[str] = None

    hourly_tokens: int = 10

    intro_video_url: Optional[str] = None

    resume_url: Optional[str] = None


# -----------------------------
# Update Tutor Profile
# -----------------------------

class TutorProfileUpdate(BaseModel):

    experience_years: Optional[int] = None

    education: Optional[str] = None

    teaching_style: Optional[str] = None

    languages: Optional[str] = None

    hourly_tokens: Optional[int] = None

    intro_video_url: Optional[str] = None

    resume_url: Optional[str] = None


# -----------------------------
# Response
# -----------------------------

class TutorProfileResponse(BaseModel):

    experience_years: Optional[int]

    education: Optional[str]

    teaching_style: Optional[str]

    languages: Optional[str]

    hourly_tokens: int

    intro_video_url: Optional[str]

    resume_url: Optional[str]

    class Config:
        from_attributes = True