from pydantic import BaseModel
from typing import List, Optional


class Answer(BaseModel):
    question_id: int
    selected: str


class SubmitTest(BaseModel):

    topic_id: Optional[int] = None
    topic_name: Optional[str] = None

    type: str

    question_ids: List[int]

    answers: List[Answer]