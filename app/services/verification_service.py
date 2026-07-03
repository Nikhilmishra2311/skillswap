from datetime import datetime, timedelta

from fastapi import HTTPException

from sqlmodel import Session, select
from app.models.test_attempt_question import TestAttemptQuestion
from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.test_answer import TestAnswer
from app.models.user_skill import UserSkill
from app.models.user import User
from app.models.topic import Topic

from app.services.question_service import get_random_questions
from app.tasks.email_tasks import tutor_verified_email_task
from app.tasks.notification_tasks import send_notification_task

from app.core.config import settings

def get_active_attempt(

    db: Session,

    user_skill_id: int

):

    return db.exec(

        select(TestAttempt).where(

            TestAttempt.user_skill_id == user_skill_id,

            TestAttempt.is_completed == False

        )

    ).first()




def get_user_skill(

    db: Session,

    user_id: int,

    topic_id: int | None = None,

    topic_name: str | None = None

):

    # -------------------------------------
    # Validation
    # -------------------------------------

    if not topic_id and not topic_name:

        raise HTTPException(

            status_code=400,

            detail="Provide topic_id or topic_name."

        )

    # -------------------------------------
    # Resolve Topic Name
    # -------------------------------------

    if topic_name:

        topic = db.exec(

            select(Topic).where(

                Topic.name.ilike(topic_name)

            )

        ).first()

        if not topic:

            raise HTTPException(

                status_code=404,

                detail="Topic not found."

            )

        topic_id = topic.id

    # -------------------------------------
    # Find Tutor Skill
    # -------------------------------------

    user_skill = db.exec(

        select(UserSkill).where(

            UserSkill.user_id == user_id,

            UserSkill.topic_id == topic_id,

            UserSkill.type == "teach"

        )

    ).first()

    if not user_skill:

        raise HTTPException(

            status_code=404,

            detail="You are not registered as tutor for this topic."

        )

    return user_skill






def start_verification(

    db: Session,

    user,

    user_skill

):

    active = get_active_attempt(db, user_skill.id)

    if active:

        raise HTTPException(
            status_code=400,
            detail="You already have an active verification attempt."
        )

    if user_skill.is_verified:
        raise HTTPException(
            status_code=400,
            detail="This topic is already verified."
        )

    questions = get_random_questions(
        db,
        topic_id=user_skill.topic_id
    )

    attempt = TestAttempt(

    user_id=user.id,

    user_skill_id=user_skill.id,

    topic_id=user_skill.topic_id,

    total_questions=len(questions),

    expires_at=datetime.utcnow() + timedelta(minutes=20)

)

    db.add(attempt)

    db.commit()

    db.refresh(attempt)

    # -----------------------------
    # Save Question Mapping
    # -----------------------------

    for index, question in enumerate(questions, start=1):

        db.add(

            TestAttemptQuestion(

                attempt_id=attempt.id,

                question_id=question.id,

                question_order=index

            )

        )

    db.commit()

    return attempt, questions














def get_attempt_questions(

    db: Session,

    attempt_id: int

):

    mappings = db.exec(

        select(TestAttemptQuestion).where(

            TestAttemptQuestion.attempt_id == attempt_id

        )

    ).all()

    question_ids = [

        m.question_id

        for m in mappings

    ]

    questions = db.exec(

        select(Question).where(

            Question.id.in_(question_ids)

        )

    ).all()

    return {

        q.id: q

        for q in questions

    }


def calculate_score(

    answers,

    question_map

):

    correct = 0

    evaluated = []

    for answer in answers:

        question = question_map.get(answer.question_id)

        if not question:

            continue

        is_correct = (

            answer.answer.lower()

            ==

            question.correct_answer.lower()

        )

        if is_correct:

            correct += 1

        evaluated.append({

            "question": question,

            "selected": answer.answer,

            "correct": is_correct

        })

    return correct, evaluated


def submit_verification(

    db: Session,

    attempt_id: int,

    answers

):

    attempt = db.get(

        TestAttempt,

        attempt_id

    )

    if not attempt:

        raise HTTPException(

            status_code=404,

            detail="Attempt not found."

        )

    if attempt.is_completed:

        raise HTTPException(

            status_code=400,

            detail="Attempt already submitted."

        )

    if datetime.utcnow() > attempt.expires_at:

        raise HTTPException(

            status_code=400,

            detail="Time expired."

        )

    question_map = get_attempt_questions(

        db,

        attempt.id

    )

    if not question_map:

        raise HTTPException(

            status_code=404,

            detail="Questions not found."

        )

    correct, evaluated = calculate_score(

        answers,

        question_map

    )

    percentage = (

        correct

        /

        len(question_map)

    ) * 100

    passed = (

        percentage

        >=

        settings.VERIFICATION_PASS_PERCENTAGE

    )

    attempt.correct_answers = correct

    attempt.percentage = percentage

    attempt.passed = passed

    attempt.is_completed = True

    attempt.submitted_at = datetime.utcnow()

    db.add(attempt)

    for item in evaluated:

        db.add(

            TestAnswer(

                attempt_id=attempt.id,

                question_id=item["question"].id,

                selected_answer=item["selected"],

                correct_answer=item["question"].correct_answer,

                is_correct=item["correct"]

            )

        )

    if passed:

        user_skill = db.get(

            UserSkill,

            attempt.user_skill_id

        )

        user_skill.is_verified = True

        db.add(user_skill)

        user = db.get(

            User,

            attempt.user_id

        )

        topic = db.get(

            Topic,

            user_skill.topic_id

        )

        if user and topic:

            tutor_verified_email_task.delay(

                user.email,

                user.full_name,

                topic.name

            )

            send_notification_task.delay(

                user.id,

                "Tutor Verified",

                f"You are now verified for {topic.name}.",

                "verification"

            )
    
    db.commit()

    return {

        "score": correct,

        "total": len(question_map),

        "percentage": percentage,

        "passed": passed

    }



