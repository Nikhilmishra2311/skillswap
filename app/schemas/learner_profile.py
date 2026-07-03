from typing import Optional

from pydantic import BaseModel


# -----------------------------
# Create Learner Profile
# -----------------------------

class LearnerProfileCreate(BaseModel):

    learning_goal: Optional[str] = None

    preferred_language: Optional[str] = None

    education_level: Optional[str] = None

    current_level: Optional[str] = None


# -----------------------------
# Update Learner Profile
# -----------------------------

class LearnerProfileUpdate(BaseModel):

    learning_goal: Optional[str] = None

    preferred_language: Optional[str] = None

    education_level: Optional[str] = None

    current_level: Optional[str] = None


# -----------------------------
# Response
# -----------------------------

class LearnerProfileResponse(BaseModel):

    learning_goal: Optional[str]

    preferred_language: Optional[str]

    education_level: Optional[str]

    current_level: Optional[str]

    class Config:
        from_attributes = True