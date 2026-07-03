from typing import Optional

from pydantic import BaseModel


from typing import Optional

class QuestionCreate(BaseModel):

    topic_id: Optional[int] = None

    topic_name: Optional[str] = None

    level: str

    question: str

    option_a: str

    option_b: str

    option_c: str

    option_d: str

    correct_answer: str

    explanation: Optional[str] = None


class QuestionUpdate(BaseModel):

    topic_id: Optional[int] = None

    topic_name: Optional[str] = None

    level: Optional[str] = None

    question: Optional[str] = None

    option_a: Optional[str] = None

    option_b: Optional[str] = None

    option_c: Optional[str] = None

    option_d: Optional[str] = None

    correct_answer: Optional[str] = None

    explanation: Optional[str] = None

    is_active: Optional[bool] = None


class AIGenerateQuestions(BaseModel):

    topic_id: Optional[int] = None

    topic_name: Optional[str] = None

    beginner_count: int = 0

    intermediate_count: int = 0

    advanced_count: int = 0


