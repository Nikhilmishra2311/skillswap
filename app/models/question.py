from sqlmodel import SQLModel, Field
from typing import Optional

class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    topic_id: int = Field(foreign_key="topic.id")

    level: str  # beginner / intermediate / advanced

    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    correct_answer: str