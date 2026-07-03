from sqlmodel import Session, select

from app.models.profile import Profile
from app.models.tutor_profile import TutorProfile
from app.models.learner_profile import LearnerProfile


def calculate_profile_completion(
    db: Session,
    user_id: int
):

    score = 0

    profile = db.exec(
        select(Profile).where(
            Profile.user_id == user_id
        )
    ).first()

    tutor = db.exec(
        select(TutorProfile).where(
            TutorProfile.user_id == user_id
        )
    ).first()

    learner = db.exec(
        select(LearnerProfile).where(
            LearnerProfile.user_id == user_id
        )
    ).first()

    # -----------------------------
    # Common Profile (60%)
    # -----------------------------

    if profile:

        if profile.full_name:
            score += 10

        if profile.bio:
            score += 10

        if profile.profile_picture:
            score += 15

        if profile.github_url:
            score += 10

        if profile.linkedin_url:
            score += 10

        if profile.website_url:
            score += 5

    # -----------------------------
    # Tutor Profile (20%)
    # -----------------------------

    if tutor:

        if tutor.experience_years is not None:
            score += 5

        if tutor.education:
            score += 5

        if tutor.teaching_style:
            score += 5

        if tutor.languages:
            score += 5

    # -----------------------------
    # Learner Profile (20%)
    # -----------------------------

    if learner:

        if learner.learning_goal:
            score += 10

        if learner.education_level:
            score += 5

        if learner.preferred_language:
            score += 5

    return min(score, 100)