from fastapi import HTTPException
from sqlmodel import Session, select

from app.models.user_skill import UserSkill
from app.models.user import User
from app.models.topic import Topic

def is_tutor(db: Session, user_id: int, topic_id: int) -> bool:
    result = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach"
        )
    ).first()

    return result is not None


def is_learner(db: Session, user_id: int, topic_id: int) -> bool:
    result = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "learn"
        )
    ).first()

    return result is not None






def remove_tutor_skill(
    db: Session,
    user_id: int,
    topic_id: int
):

    skill = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach"
        )
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Tutor skill not found"
        )

    db.delete(skill)
    db.commit()

    return {
        "message": "Tutor skill removed successfully"
    }







def add_user_skill(
    db: Session,
    user_id: int,
    topic_id: int | None = None,
    topic_name: str | None = None,
    type: str = "",
    level: str | None = None
):

    # Must provide either topic_id or topic_name
    if not topic_id and not topic_name:
        raise HTTPException(
            status_code=400,
            detail="Provide either topic_id or topic_name"
        )

    # Find topic using name
    if topic_name:
        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(topic_name)
            )
        ).first()

        if not topic:
            raise HTTPException(
                status_code=404,
                detail="Topic not found"
            )

        topic_id = topic.id

    # Prevent duplicate registration
    existing = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == type
        )
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already registered for this topic"
        )

    # Tutor Registration
    if type == "teach":

        if not level:
            raise HTTPException(
                status_code=400,
                detail="Level required for tutor"
            )

        is_verified = False

    # Learner Registration
    elif type == "learn":

        level = None
        is_verified = True

        # Give starter tokens only first time
        existing_learn = db.exec(
            select(UserSkill).where(
                UserSkill.user_id == user_id,
                UserSkill.type == "learn"
            )
        ).first()

        if not existing_learn:

            user = db.get(User, user_id)

            if user and user.token_balance == 0:
                user.token_balance = 100
                db.add(user)

    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid type"
        )

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