from typing import Optional
from sqlmodel import SQLModel, Field


class AvailabilitySlot(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int

    day: str

    start_time: str

    end_time: str

    is_active: bool = True