from sqlmodel import select

from app.models.user import User
from app.models.session import Session
from app.models.user_skill import UserSkill
from app.models.question import Question
from app.models.topic import Topic
from app.models.token_transaction import TokenTransaction


def get_admin_dashboard(db):

    users = db.exec(
        select(User)
    ).all()

    sessions = db.exec(
        select(Session)
    ).all()

    completed_sessions = db.exec(
        select(Session).where(
            Session.status == "completed"
        )
    ).all()

    verified_tutors = db.exec(
        select(UserSkill).where(
            UserSkill.is_verified == True
        )
    ).all()

    questions = db.exec(
        select(Question)
    ).all()

    topics = db.exec(
        select(Topic)
    ).all()

    transactions = db.exec(
        select(TokenTransaction)
    ).all()

    total_tokens = sum(
        tx.amount
        for tx in transactions
    )

    return {

        "total_users":
        len(users),

        "total_sessions":
        len(sessions),

        "completed_sessions":
        len(completed_sessions),

        "verified_tutors":
        len(verified_tutors),

        "questions":
        len(questions),

        "topics":
        len(topics),

        "tokens_transferred":
        total_tokens
    }

def get_user_stats(db):

    users = db.exec(
        select(User)
    ).all()

    tutors = 0
    learners = 0

    for user in users:

        teach_skill = db.exec(
            select(UserSkill).where(
                UserSkill.user_id == user.id,
                UserSkill.type == "teach"
            )
        ).first()

        learn_skill = db.exec(
            select(UserSkill).where(
                UserSkill.user_id == user.id,
                UserSkill.type == "learn"
            )
        ).first()

        if teach_skill:
            tutors += 1

        if learn_skill:
            learners += 1

    return {
        "tutors": tutors,
        "learners": learners
    }


def get_all_users(db):
    """Return all users."""
    return db.exec(select(User)).all()


def get_all_tutors(db):
    """Return users who have a teach UserSkill."""
    tutor_ids = db.exec(
        select(UserSkill.user_id).where(
            UserSkill.type == "teach"
        )
    ).all()

    # Ensure unique ids
    tutor_ids = list(set(tutor_ids))

    if not tutor_ids:
        return []

    return db.exec(
        select(User).where(
            User.id.in_(tutor_ids)
        )
    ).all()