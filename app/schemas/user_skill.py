from pydantic import BaseModel
from typing import Optional


class UserSkillCreate(BaseModel):
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None

    type: str
    level: Optional[str] = None