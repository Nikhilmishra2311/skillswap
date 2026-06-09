from sqlmodel import Session, select

from app.models.user_skill import UserSkill
from app.models.user import User


def find_tutors_for_topic(
    db: Session,
    learner_id: int,
    topic_id: int
):
    tutor_skills = db.exec(
        select(UserSkill).where(
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach",
            UserSkill.is_verified == True
        )
    ).all()

    tutors = []

    for skill in tutor_skills:

        # learner khud ko match na kare
        if skill.user_id == learner_id:
            continue

        tutor = db.get(User, skill.user_id)

        if tutor:
            tutors.append({
                "tutor_id": tutor.id,
                "email": tutor.email,
                "level": skill.level,
                "verified": skill.is_verified
            })

    return tutors