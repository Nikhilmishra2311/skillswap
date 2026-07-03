from sqlmodel import Session, select

from app.models.profile import Profile
from app.models.notification import Notification
from app.models.session import Session as LearningSession
from app.models.user import User

from app.services.profile_completion_service import (
    calculate_profile_completion
)


def get_dashboard(
    db: Session,
    user_id: int
):

    user = db.get(
        User,
        user_id
    )

    if not user:
        raise Exception(
            "User not found"
        )

    profile = db.exec(
        select(Profile).where(
            Profile.user_id == user_id
        )
    ).first()

    notifications = db.exec(
        select(Notification)
        .where(
            Notification.user_id == user_id
        )
        .order_by(
            Notification.created_at.desc()
        )
    ).all()

    completed_sessions = db.exec(
        select(LearningSession).where(
            LearningSession.status == "completed",
            (
                (LearningSession.tutor_id == user_id)
                |
                (LearningSession.learner_id == user_id)
            )
        )
    ).all()

    profile_completion = calculate_profile_completion(
        db,
        user_id
    )

    next_step = get_next_step(
        profile_completion
    )

    return {

        "user": {

            "id": user.id,

            "email": user.email,

            "role": user.role

        },

        "profile": profile,

        "profile_completion": profile_completion,

        "next_step": next_step,

        "token_balance": user.token_balance,

        "completed_sessions": len(
            completed_sessions
        ),

        "notifications": notifications

    }

def get_next_step(
    completion: int
):

    if completion == 100:

        return "Profile Completed"

    if completion < 20:

        return "Complete your basic profile."

    if completion < 50:

        return "Upload your profile picture."

    if completion < 80:

        return "Complete your tutor/learner profile."

    return "Almost done."