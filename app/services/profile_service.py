from sqlmodel import Session, select

from app.models.profile import Profile

from app.services.storage_service import get_file_url
def get_my_profile(
    db: Session,
    user_id: int
):

    profile = db.exec(
        select(Profile).where(
            Profile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception("Profile not found")

    if profile.profile_picture:

        profile.profile_picture = get_file_url(
            profile.profile_picture
        )

    return profile



def get_profile_by_user_id(
    db: Session,
    user_id: int
):

    profile = db.exec(
        select(Profile).where(
            Profile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception("Profile not found")

    if profile.profile_picture:

        profile.profile_picture = get_file_url(
            profile.profile_picture
        )

    return profile


def update_profile(
    db: Session,
    user_id: int,
    data,
    profile_picture: str | None = None
):

    profile = db.exec(
        select(Profile).where(
            Profile.user_id == user_id
        )
    ).first()

    if not profile:
        raise Exception("Profile not found")

    updates = data.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():
        setattr(profile, key, value)

    if profile_picture:
        profile.profile_picture = profile_picture

    db.add(profile)

    db.commit()

    db.refresh(profile)
    if profile.profile_picture:

      profile.profile_picture = get_file_url(
        profile.profile_picture
    )
    return profile