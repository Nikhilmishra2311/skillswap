from fastapi import APIRouter, Depends, HTTPException
from app.models.session import Session
from app.models.session import Session
from sqlmodel import Session as DBSession
from app.services.session_service import complete_session, get_available_sessions
from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.user_skill_service import is_tutor, is_learner 
from app.services.session_service import create_session, book_session
from app.schemas.session import CreateSession
from app.services.session_service import start_session

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# 🔥 Tutor creates session
@router.post("/create")
def create_session_api(
    data: CreateSession,
    db: DBSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    # ✅ Check tutor permission
    if not is_tutor(db, current_user.id, data.topic_id):
        raise HTTPException(
            status_code=403,
            detail="You are not a verified tutor for this topic"
        )

    try:
        return create_session(
            db,
            current_user.id,
            data.topic_id,
            data.start_time
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.post("/start/{session_id}")
def start_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    try:
        return start_session(db, session_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@router.get("/available/{topic_id}")
def available_sessions(
    topic_id: int,
    db: DBSession = Depends(get_session)
):
    return get_available_sessions(db, topic_id)
# 🔥 Learner books session
@router.post("/book/{session_id}")
def book_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    session = db.get(Session, session_id)

    if not session:
        raise HTTPException(404, "Session not found")

    if not is_learner(db, current_user.id, session.topic_id):
        raise HTTPException(403, "Not a learner")

    return book_session(db, session_id, current_user.id)
    
@router.post("/complete/{session_id}")
def complete_session_api(
    session_id: int,
    db: DBSession = Depends(get_session),
    current_user = Depends(get_current_user)
):
    try:
        return complete_session(db, session_id, current_user.id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))