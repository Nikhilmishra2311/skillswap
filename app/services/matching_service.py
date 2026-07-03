from sqlmodel import select

from app.models.user import User
from app.models.topic import Topic
from app.models.user_skill import UserSkill
from app.models.availability import AvailabilitySlot


def find_tutors(
    db,
    learner_id: int,
    topic_id: int | None = None,
    topic_name: str | None = None
):

    # 🔥 Topic name support
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

        # learner khud tutor ho to skip
        if skill.user_id == learner_id:
            continue

        tutor = db.get(
            User,
            skill.user_id
        )

        if not tutor:
            continue

        topic = db.get(
            Topic,
            skill.topic_id
        )

        # 🔥 Tutor availability
        availability = db.exec(
            select(AvailabilitySlot).where(
                AvailabilitySlot.user_id == tutor.id,
                AvailabilitySlot.is_active == True
            )
        ).all()

        tutors.append({
            "tutor_id": tutor.id,
            "email": tutor.email,
            "topic_id": skill.topic_id,
            "topic_name": topic.name if topic else None,
            "level": skill.level,
            "verified": skill.is_verified,

            "availability": [
                {
                    "day": slot.day,
                    "start_time": slot.start_time,
                    "end_time": slot.end_time
                }
                for slot in availability
            ]
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

    for learner_skill in learner_topics:

        topic = db.get(
            Topic,
            learner_skill.topic_id
        )

        tutor_skills = db.exec(
            select(UserSkill).where(
                UserSkill.topic_id == learner_skill.topic_id,
                UserSkill.type == "teach",
                UserSkill.is_verified == True
            )
        ).all()

        formatted_tutors = []

        for tutor_skill in tutor_skills:

            if tutor_skill.user_id == learner_id:
                continue

            tutor = db.get(
                User,
                tutor_skill.user_id
            )

            if not tutor:
                continue

            availability = db.exec(
                select(AvailabilitySlot).where(
                    AvailabilitySlot.user_id == tutor.id,
                    AvailabilitySlot.is_active == True
                )
            ).all()

            formatted_tutors.append({
                "tutor_id": tutor.id,
                "email": tutor.email,
                "level": tutor_skill.level,

                "availability": [
                    {
                        "day": slot.day,
                        "start_time": slot.start_time,
                        "end_time": slot.end_time
                    }
                    for slot in availability
                ]
            })

        result.append({
            "topic_id": learner_skill.topic_id,
            "topic_name": topic.name if topic else None,
            "tutors": formatted_tutors
        })

    return result