from pydantic import BaseModel


class QuestionPublic(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str