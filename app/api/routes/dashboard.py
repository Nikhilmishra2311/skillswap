from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user
from app.db.session import get_session

from app.services.dashboard_service import (
    get_dashboard
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    try:

        return get_dashboard(
            db,
            current_user.id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )