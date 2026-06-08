from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.user_skill_service import add_user_skill

router = APIRouter(prefix="/user-skills", tags=["User Skills"])


@router.post("/tutor")
def add_tutor_skill(
    topic_id: int,
    level: str,
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    try:
        return add_user_skill(
            db=db,
            user_id=current_user.id,
            topic_id=topic_id,
            type="teach",
            level=level
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.post("/learner")
def add_learner_skill(
    topic_id: int,
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    try:
        return add_user_skill(
            db=db,
            user_id=current_user.id,
            topic_id=topic_id,
            type="learn",
            level=None
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))