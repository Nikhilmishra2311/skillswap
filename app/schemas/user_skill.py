from pydantic import BaseModel
from typing import Optional

class UserSkillCreate(BaseModel):
    topic_id: int
    type: str
    level: Optional[str] = None