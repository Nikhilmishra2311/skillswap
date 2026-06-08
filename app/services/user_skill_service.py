from sqlmodel import Session, select
from app.models.user_skill import UserSkill


def is_tutor(db: Session, user_id: int, topic_id: int) -> bool:
    """Check if user is a tutor for the given topic."""
    result = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach"
        )
    ).first()
    return result is not None


def is_learner(db: Session, user_id: int, topic_id: int) -> bool:
    """Check if user is a learner for the given topic."""
    result = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "learn"
        )
    ).first()
    return result is not None


def add_user_skill(db, user_id, topic_id, type, level=None):

    # 🔥 Tutor
    if type == "teach":
        if not level:
            raise HTTPException(400, "Level required for tutor")
        is_verified = False   # test required

    # 🔥 Learner
    elif type == "learn":
        level = None
        is_verified = True   # auto verified

    else:
        raise HTTPException(400, "Invalid type")

    user_skill = UserSkill(
        user_id=user_id,
        topic_id=topic_id,
        type=type,
        level=level,
        is_verified=is_verified
    )

    db.add(user_skill)
    db.commit()
    db.refresh(user_skill)

    return user_skill