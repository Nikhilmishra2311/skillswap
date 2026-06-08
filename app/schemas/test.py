from pydantic import BaseModel
from typing import List


class Answer(BaseModel):
    question_id: int
    selected: str


class SubmitTest(BaseModel):
    topic_id: int
    answers: List[Answer]