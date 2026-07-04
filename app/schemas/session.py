from datetime import date, time
from typing import Optional
from pydantic import BaseModel

class CreateSession(BaseModel):

    topic_id: Optional[int] = None
    topic_name: Optional[str] = None

    session_date: date
    session_time: time