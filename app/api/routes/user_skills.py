from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session,select

from app.models.topic import Topic

from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.user_skill_service import add_user_skill

router = APIRouter(
    prefix="/user-skills",
    tags=["User Skills"]
)


@router.delete("/tutor")
def delete_tutor_skill(
    topic_id: int | None = None,
    topic_name: str | None = None,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    if topic_name:

        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(topic_name)
            )
        ).first()

        if not topic:
            raise HTTPException(
                status_code=404,
                detail="Topic not found"
            )

        topic_id = topic.id

    if not topic_id:
        raise HTTPException(
            status_code=400,
            detail="Provide topic_id or topic_name"
        )

    return remove_tutor_skill(
        db,
        current_user.id,
        topic_id
    )

@router.post("/tutor")
def add_tutor_skill(
    topic_id: int | None = None,
    topic_name: str | None = None,
    level: str | None = None,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    try:
        return add_user_skill(
            db=db,
            user_id=current_user.id,
            topic_id=topic_id,
            topic_name=topic_name,
            type="teach",
            level=level
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/learner")
def add_learner_skill(
    topic_id: int | None = None,
    topic_name: str | None = None,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    try:
        return add_user_skill(
            db=db,
            user_id=current_user.id,
            topic_id=topic_id,
            topic_name=topic_name,
            type="learn",
            level=None
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )