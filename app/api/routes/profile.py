from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.profile_service import get_tutor_profile

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/me")
def my_profile(
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    return get_tutor_profile(db, current_user.id)


@router.get("/{user_id}")
def view_profile(
    user_id: int,
    db: Session = Depends(get_session)
):
    return get_tutor_profile(db, user_id)