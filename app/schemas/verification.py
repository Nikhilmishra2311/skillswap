from pydantic import BaseModel
from typing import List

from typing import Optional
# ==========================================
# Start Verification
# ==========================================

class StartVerificationRequest(BaseModel):

    topic_id: Optional[int] = None

    topic_name: Optional[str] = None


# ==========================================
# Question Response
# ==========================================

class VerificationQuestion(BaseModel):

    id: int

    question: str

    option_a: str

    option_b: str

    option_c: str

    option_d: str


# ==========================================
# Start Verification Response
# ==========================================

class StartVerificationResponse(BaseModel):

    attempt_id: int

    duration: int

    questions: List[VerificationQuestion]


# ==========================================
# Submit Answer
# ==========================================

class AnswerItem(BaseModel):

    question_id: int

    answer: str


class SubmitVerificationRequest(BaseModel):

    attempt_id: int

    answers: List[AnswerItem]


# ==========================================
# Submit Result
# ==========================================

class SubmitVerificationResponse(BaseModel):

    total_questions: int

    correct_answers: int

    percentage: float

    passed: bool