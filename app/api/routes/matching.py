from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user

from app.services.matching_service import (
    find_tutors_for_topic
)

router = APIRouter(
    prefix="/matching",
    tags=["Matching"]
)


@router.get("/{topic_id}")
def get_matching_tutors(
    topic_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    return find_tutors_for_topic(
        db,
        current_user.id,
        topic_id
    )