from fastapi import APIRouter, Depends

from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user

from app.services.notification_service import (
    get_notifications,
    mark_notification_read
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/")
def my_notifications(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return get_notifications(
        db,
        current_user.id
    )

@router.patch("/{notification_id}/read")
def mark_read(
    notification_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return mark_notification_read(
        db,
        notification_id,
        current_user.id
    )