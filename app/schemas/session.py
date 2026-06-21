from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class CreateSession(BaseModel):
    topic_id: Optional[int] = None
    topic_name: Optional[str] = None 
    start_time: datetime