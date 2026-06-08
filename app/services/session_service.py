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


def complete_session(db: DBSession, session_id: int, user_id: int):

    session = db.get(Session, session_id)

    if session.tutor_id != user_id:
        raise Exception("Only tutor")

    if session.status != "ongoing":
        raise Exception("Not ongoing")

    learner = db.get(User, session.learner_id)
    tutor = db.get(User, session.tutor_id)

    if learner.token_balance < TOKEN_PER_SESSION:
        raise Exception("Insufficient tokens")

    learner.token_balance -= TOKEN_PER_SESSION
    tutor.token_balance += TOKEN_PER_SESSION

    txn = TokenTransaction(
        sender_id=learner.id,
        receiver_id=tutor.id,
        amount=TOKEN_PER_SESSION,
        session_id=session.id
    )

    session.status = "completed"

    db.add_all([learner, tutor, txn, session])
    db.commit()

    return {"message": "completed"}