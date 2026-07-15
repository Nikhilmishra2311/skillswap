from fastapi import APIRouter
from fastapi import Depends,Request
from fastapi import HTTPException
from app.core.limiter import limiter
from sqlmodel import Session

from app.db.session import get_session

from app.api.deps import get_current_user

from app.schemas.availability import (
    AvailabilityCreate
)
from app.schemas.availability import UpdateAvailability

from app.services.availability_service import update_availability

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
@limiter.limit("20/minute")
def add_slot(
    request: Request,
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
@limiter.limit("60/minute")
def my_slots(
    request: Request,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return get_my_availability(
        db,
        current_user.id
    )

@router.get("/user/{user_id}")
@limiter.limit("60/minute")
def tutor_availability(
    request: Request,
    user_id: int,
    db: Session = Depends(get_session)
):

    return get_user_availability(
        db,
        user_id
    )

@router.put("/{availability_id}")
@limiter.limit("30/minute")
def update_availability_api(

    request: Request,
    availability_id: int,

    data: UpdateAvailability,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    return update_availability(

        db,

        availability_id,

        current_user.id,

        data
    )


@router.delete("/{slot_id}")
@limiter.limit("20/minute")
def remove_slot(
    request: Request,
    slot_id: int,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return delete_availability(
        db,
        slot_id,
        current_user.id
    )