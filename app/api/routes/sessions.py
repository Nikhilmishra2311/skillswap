from fastapi import APIRouter, Depends, HTTPException
from app.models.session import Session
from sqlmodel import Session as DBSession, select
from datetime import datetime
from fastapi import Depends

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.user import User
from app.models.topic import Topic  # 🔥 NEW
from app.services.session_service import (
    complete_session,
    get_available_sessions,
    create_session,
    book_session,
    start_session,
    cancel_session,
    get_my_created_sessions,
    get_my_booked_sessions,
    get_session_history,
    get_session_details,
    get_meeting
)

from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.user_skill_service import (
    is_tutor,
    is_learner
)

from app.schemas.session import CreateSession

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"]
)


# 🔥 Tutor creates session
@router.post("/create")
def create_session_api(
    data: CreateSession,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    # ===================================================
    # 🔥 NEW : topic_id ya topic_name dono support karna
    # ===================================================

    topic_id = data.topic_id

    if data.topic_name:

        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(data.topic_name)
            )
        ).first()

        if not topic:
            raise HTTPException(
                status_code=404,
                detail="Topic not found"
            )

        topic_id = topic.id

    # ===================================================
    # 🔥 NEW : validation
    # ===================================================

    if not topic_id:
        raise HTTPException(
            status_code=400,
            detail="Provide topic_id or topic_name"
        )

    # ===================================================
    # 🔥 Tutor verification check
    # ===================================================

    if not is_tutor(
        db,
        current_user.id,
        topic_id
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not a verified tutor for this topic"
        )

    try:
        start_time = datetime.combine(
            data.session_date,
            data.session_time
        )

        return create_session(
            db,
            current_user.id,
            topic_id,
            start_time
        )

    except Exception as e:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=400,
            detail=f"{type(e).__name__}: {e!r}"
        )


@router.post("/start/{session_id}")
def start_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):
    try:
        return start_session(
            db,
            session_id,
            current_user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/{session_id}/meeting")
def meeting_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):
    try:

        return get_meeting(
            db,
            session_id,
            current_user.id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
@router.get("/available")
def available_sessions(
    topic_id: int | None = None,
    topic_name: str | None = None,
    db: DBSession = Depends(get_session)
):
    return get_available_sessions(
        db,
        topic_id,
        topic_name
    )


# 🔥 Learner books session
@router.post("/book/{session_id}")
def book_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    session = db.get(
        Session,
        session_id
    )

    if not session:
        raise HTTPException(
            404,
            "Session not found"
        )

    if not is_learner(
        db,
        current_user.id,
        session.topic_id
    ):
        raise HTTPException(
            403,
            "Not a learner"
        )

    return book_session(
        db,
        session_id,
        current_user.id
    )


@router.post("/complete/{session_id}")
def complete_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):
    try:
        return complete_session(
            db,
            session_id,
            current_user.id
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    


# =====================================
# Cancel Session
# =====================================

@router.post("/cancel/{session_id}")
def cancel_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    try:

        return cancel_session(
            db,
            session_id,
            current_user.id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
# =====================================
# My Created Sessions (Tutor)
# =====================================

@router.get("/my-created")
def my_created_sessions_api(
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return get_my_created_sessions(
        db,
        current_user.id
    )

# =====================================
# My Booked Sessions (Learner)
# =====================================

@router.get("/my-booked")
def my_booked_sessions_api(
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return get_my_booked_sessions(
        db,
        current_user.id
    )
@router.get("/{session_id}/join")
def join_session(

    session_id: int,

    db: DBSession = Depends(get_session),
    current_user: User = Depends(get_current_user)

):

    return session_service.join_session(
        db=db,
        session_id=session_id,
        user_id=current_user.id

    )
# =====================================
# Session History
# =====================================

@router.get("/history")
def session_history_api(
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    return get_session_history(
        db,
        current_user.id
    )

# =====================================
# Session Details
# =====================================

@router.get("/{session_id}")
def session_details_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user=Depends(get_current_user)
):

    try:

        return get_session_details(
            db,
            session_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    