from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlmodel import Session

from app.db.session import get_session

from app.api.deps import get_current_user

from app.schemas.availability import (
    AvailabilityCreate
)

from app.services.availability_service import (
    create_availability,
    get_my_availability,
    delete_availability,
    get_user_availability
)

router = APIRouter(
    prefix="/availability",
    tags=["Availability"]
)


@router.post("/")
def add_slot(
    data: AvailabilityCreate,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    try:

        return create_availability(
            db,
            current_user.id,
            data.day,
            data.start_time,
            data.end_time
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/me")
def my_slots(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return get_my_availability(
        db,
        current_user.id
    )

@router.get("/user/{user_id}")
def tutor_availability(
    user_id: int,
    db: Session = Depends(get_session)
):

    return get_user_availability(
        db,
        user_id
    )
@router.delete("/{slot_id}")
def remove_slot(
    slot_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return delete_availability(
        db,
        slot_id,
        current_user.id
    )