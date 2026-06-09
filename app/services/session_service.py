from sqlmodel import Session as DBSession, select
from app.models.session import Session
from app.models.user import User
from app.models.token_transaction import TokenTransaction
from app.models.user_skill import UserSkill

TOKEN_PER_SESSION = 10


def create_session(db: DBSession, tutor_id: int, topic_id: int, start_time):

    user_skill = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == tutor_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach",
            UserSkill.is_verified == True
        )
    ).first()

    if not user_skill:
        raise Exception("Not a verified tutor")

    session = Session(
        tutor_id=tutor_id,
        topic_id=topic_id,
        start_time=start_time,
        status="open"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_available_sessions(db: DBSession, topic_id: int):
    return db.exec(
        select(Session).where(
            Session.topic_id == topic_id,
            Session.status == "open"
        )
    ).all()


def book_session(db: DBSession, session_id: int, learner_id: int):

    session = db.get(Session, session_id)

    if not session:
        raise Exception("Session not found")

    if session.status != "open":
        raise Exception("Session not available")

    if session.tutor_id == learner_id:
        raise Exception("Cannot book your own session")

    session.learner_id = learner_id
    session.status = "booked"

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def start_session(db: DBSession, session_id: int, user_id: int):

    session = db.get(Session, session_id)

    if session.tutor_id != user_id:
        raise Exception("Only tutor can start")

    if session.status != "booked":
        raise Exception("Not ready")

    session.status = "ongoing"

    db.commit()
    return session


def complete_session(
    db: DBSession,
    session_id: int,
    tutor_id: int
):
    session = db.get(Session, session_id)

    if not session:
        raise Exception("Session not found")

    if session.tutor_id != tutor_id:
        raise Exception("Only tutor can complete session")

    if session.status != "started":
        raise Exception("Session must be started first")

    learner = db.get(User, session.learner_id)
    tutor = db.get(User, session.tutor_id)

    SESSION_COST = 10

    if learner.token_balance < SESSION_COST:
        raise Exception("Learner has insufficient tokens")

    learner.token_balance -= SESSION_COST
    tutor.token_balance += SESSION_COST

    transaction = TokenTransaction(
        sender_id=learner.id,
        receiver_id=tutor.id,
        session_id=session.id,
        amount=SESSION_COST
    )

    db.add(transaction)

    session.status = "completed"

    db.add(learner)
    db.add(tutor)
    db.add(session)

    db.commit()

    db.refresh(session)

    return {
        "message": "Session completed successfully",
        "tokens_transferred": SESSION_COST,
        "session_id": session.id
    }