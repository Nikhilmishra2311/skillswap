from fastapi import APIRouter, Depends
from fastapi import Request
from app.core.limiter import limiter
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
@limiter.limit("60/minute")
def notifications(

    request: Request,

    page: int = 1,

    size: int = 10,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return get_notifications(

        db,

        current_user.id,

        page,

        size

    )

@router.patch("/{notification_id}/read")
@limiter.limit("60/minute")
def mark_read(
    request: Request,
    notification_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return mark_notification_read(
        db,
        notification_id,
        current_user.id
    )