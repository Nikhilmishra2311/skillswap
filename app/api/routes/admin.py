from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import (
    get_current_user
)

from app.services.admin_service import (
    get_admin_dashboard,
    get_all_users,
    get_all_tutors
)

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

def require_admin(user):

    if user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )
    


@router.get("/dashboard")
def admin_dashboard(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    require_admin(
        current_user
    )

    return get_admin_dashboard(
        db
    )

@router.get("/users")
def users(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    require_admin(current_user)

    return get_all_users(db)

@router.get("/tutors")
def tutors(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    require_admin(current_user)

    return get_all_tutors(db)


