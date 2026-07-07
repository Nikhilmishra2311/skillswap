from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Session(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    tutor_id: int = Field(foreign_key="user.id")

    learner_id: Optional[int] = Field(
        default=None,
        foreign_key="user.id"
    )

    topic_id: int = Field(
        foreign_key="topic.id"
    )

    availability_slot_id: Optional[int] = Field(
        default=None,
        foreign_key="availabilityslot.id"
    )

    start_time: datetime

    meeting_room_id: Optional[str] = None

    meeting_room: Optional[str] = None

    meeting_link: Optional[str] = None

    status: str = "open"