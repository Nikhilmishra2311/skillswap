from pydantic import BaseModel
from typing import List


class SkillInfo(BaseModel):
    topic_name: str
    level: str
    is_verified: bool


class TutorProfile(BaseModel):
    user_id: int
    email: str
    bio: str | None
    skills: List[SkillInfo]