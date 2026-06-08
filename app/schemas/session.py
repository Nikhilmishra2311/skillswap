from pydantic import BaseModel
from datetime import datetime


class CreateSession(BaseModel):
    topic_id: int
    start_time: datetime