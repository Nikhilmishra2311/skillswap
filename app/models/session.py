from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Session(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tutor_id: int = Field(foreign_key="user.id")
    learner_id: Optional[int] = Field(default=None, foreign_key="user.id")

    topic_id: int = Field(foreign_key="topic.id")

    start_time: datetime

    status: str = "open"   # open | booked | ongoing | completed | cancelled