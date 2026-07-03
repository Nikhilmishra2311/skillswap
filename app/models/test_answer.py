from sqlmodel import SQLModel, Field
from typing import Optional


class TestAnswer(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    attempt_id: int = Field(foreign_key="testattempt.id")

    question_id: int = Field(foreign_key="question.id")

    selected_answer: str

    correct_answer: str

    is_correct: bool