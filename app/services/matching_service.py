from sqlmodel import select

from app.models.user import User
from app.models.topic import Topic
from app.models.user_skill import UserSkill

def find_tutors(
    db,
    learner_id: int,
    topic_id: int | None = None,
    topic_name: str | None = None
):

    if topic_name:

        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(topic_name)
            )
        ).first()

        if not topic:
            return []

        topic_id = topic.id

    query = select(UserSkill).where(
        UserSkill.type == "teach",
        UserSkill.is_verified == True
    )

    if topic_id:
        query = query.where(
            UserSkill.topic_id == topic_id
        )

    tutor_skills = db.exec(query).all()

    tutors = []

    for skill in tutor_skills:

        if skill.user_id == learner_id:
            continue

        tutor = db.get(User, skill.user_id)

        if tutor:
            tutors.append({
                "tutor_id": tutor.id,
                "email": tutor.email,
                "topic_id": skill.topic_id,
                "level": skill.level,
                "verified": skill.is_verified
            })

    return tutors

def my_topics_matches(
    db,
    learner_id: int
):

    learner_topics = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == learner_id,
            UserSkill.type == "learn"
        )
    ).all()

    result = []

    for item in learner_topics:

        tutors = db.exec(
            select(UserSkill).where(
                UserSkill.topic_id == item.topic_id,
                UserSkill.type == "teach",
                UserSkill.is_verified == True
            )
        ).all()

        result.append({
            "topic_id": item.topic_id,
            "tutors": tutors
        })

    return result