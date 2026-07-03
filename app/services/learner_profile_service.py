from sqlmodel import Session, select

from app.models.learner_profile import LearnerProfile
from app.models.user_skill import UserSkill


def create_learner_profile(
    db: Session,
    user_id: int,
    data
):

    skill = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.type == "learn"
        )
    ).first()

    if not skill:
        raise Exception(
            "Please add at least one learning skill first."
        )

    existing = db.exec(
        select(LearnerProfile).where(
            LearnerProfile.user_id == user_id
        )
    ).first()

    if existing:
        raise Exception(
            "Learner profile already exists."
        )

    profile = LearnerProfile(
        user_id=user_id,
        **data.model_dump()
    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile



def get_learner_profile(
    db: Session,
    user_id: int
):

    profile = db.exec(
        select(LearnerProfile).where(
            LearnerProfile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception(
            "Learner profile not found."
        )

    return profile

def update_learner_profile(
    db: Session,
    user_id: int,
    data
):

    profile = db.exec(
        select(LearnerProfile).where(
            LearnerProfile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception(
            "Learner profile not found."
        )

    updates = data.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():

        setattr(
            profile,
            key,
            value
        )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile