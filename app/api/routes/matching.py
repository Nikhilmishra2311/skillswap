from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user

from app.services.matching_service import (
    find_tutors,
    my_topics_matches
)

router = APIRouter(
    prefix="/matching",
    tags=["Matching"]
)


@router.get("/")
def match_tutors(
    topic_id: int | None = None,
    topic_name: str | None = None,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    return find_tutors(
        db,
        current_user.id,
        topic_id,
        topic_name
    )


@router.get("/my-topics")
def my_topic_matches(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    return my_topics_matches(
        db,
        current_user.id
    )