from pydantic import BaseModel

from typing import List, Optional


class GenerateQuestionRequest(BaseModel):

    topic_id: Optional[int] = None

    topic_name: Optional[str] = None

    beginner_count: int = 0

    intermediate_count: int = 0

    advanced_count: int = 0


class GeneratedQuestion(BaseModel):

    topic_id: int

    level: str

    question: str

    option_a: str

    option_b: str

    option_c: str

    option_d: str

    correct_answer: str

    explanation: Optional[str] = None


class SaveGeneratedQuestions(BaseModel):

    questions: List[GeneratedQuestion]