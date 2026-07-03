from sqlmodel import Session, select

from app.models.tutor_profile import TutorProfile



def create_tutor_profile(
    db: Session,
    user_id: int,
    data
):

    existing = db.exec(
        select(TutorProfile).where(
            TutorProfile.user_id == user_id
        )
    ).first()

    if existing:
        raise Exception(
            "Tutor profile already exists"
        )

    profile = TutorProfile(
        user_id=user_id,
        **data.model_dump()
    )

    db.add(profile)

    db.commit()

    db.refresh(profile)

    return profile

def get_tutor_profile(
    db: Session,
    user_id: int
):

    profile = db.exec(
        select(TutorProfile).where(
            TutorProfile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception(
            "Tutor profile not found"
        )

    return profile

def update_tutor_profile(
    db: Session,
    user_id: int,
    data
):

    profile = db.exec(
        select(TutorProfile).where(
            TutorProfile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception(
            "Tutor profile not found"
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