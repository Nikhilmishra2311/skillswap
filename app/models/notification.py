from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Notification(SQLModel, table=True):

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    user_id: int = Field(
        foreign_key="user.id"
    )

    title: str

    message: str

    type: str

    is_read: bool = False

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )