from sqlmodel import Session as DBSession, select
from app.models.session import Session
from app.models.user import User
from app.models.token_transaction import TokenTransaction
from app.models.user_skill import UserSkill
from app.models.topic import Topic 
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




def get_available_sessions(
    db,
    topic_id: int | None = None,
    topic_name: str | None = None
):

    # 🔥 Topic name support
    if topic_name:

        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(topic_name)
            )
        ).first()

        if not topic:
            return []

        topic_id = topic.id

    query = select(Session).where(
        Session.status == "open"
    )

    # 🔥 Filter only if topic provided
    if topic_id:
        query = query.where(
            Session.topic_id == topic_id
        )

    sessions = db.exec(query).all()

    result = []

    for session in sessions:

        tutor = db.get(
            User,
            session.tutor_id
        )

        topic = db.get(
            Topic,
            session.topic_id
        )

        result.append({
            "session_id": session.id,
            "topic": topic.name if topic else None,
            "tutor_id": tutor.id if tutor else None,
            "tutor_email": tutor.email if tutor else None,
            "status": session.status,
            "start_time": session.start_time
        })

    return result


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

    if not session:
        raise Exception("Session not found")

    if session.tutor_id != user_id:
        raise Exception("Only tutor can start")

    if session.status != "booked":
        raise Exception("Session not ready")

    session.status = "ongoing"

    db.add(session)
    db.commit()
    db.refresh(session)

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

    if session.status != "ongoing":
        raise Exception("Session must be ongoing first")

    if session.learner_id is None:
        raise Exception("No learner booked this session")

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
        "session_id": session.id,
        "learner_balance": learner.token_balance,
        "tutor_balance": tutor.token_balance
    }