from sqlmodel import SQLModel, Field
from typing import Optional

class UserSkill(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id")
    topic_id: int = Field(foreign_key="topic.id")

    type: str  # "teach" or "learn"
    level: str | None = None  # beginner / intermediate / advanced

    is_verified: bool = False