from sqlmodel import Session, select
from app.models.user import User
from app.models.user_skill import UserSkill
from app.models.topic import Topic


def get_tutor_profile(db: Session, user_id: int):
    user = db.get(User, user_id)

    skills = db.exec(
        select(UserSkill, Topic)
        .join(Topic, UserSkill.topic_id == Topic.id)
        .where(
            UserSkill.user_id == user_id,
            UserSkill.type == "teach"
        )
    ).all()

    skill_list = []

    for user_skill, topic in skills:
        skill_list.append({
            "topic_name": topic.name,
            "level": user_skill.level,
            "is_verified": user_skill.is_verified
        })

    return {
        "user_id": user.id,
        "email": user.email,
        "bio": user.bio,
        "skills": skill_list
    }