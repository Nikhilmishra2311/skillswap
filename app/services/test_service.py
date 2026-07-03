from sqlmodel import Session, select
from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.user_skill import UserSkill
from random import sample
from app.services.notification_service import create_notification


def get_questions(
    db,
    topic_id: int,
    level: str
):

    beginner_questions = db.exec(
        select(Question).where(
            Question.topic_id == topic_id,
            Question.level == "beginner"
        )
    ).all()

    intermediate_questions = db.exec(
        select(Question).where(
            Question.topic_id == topic_id,
            Question.level == "intermediate"
        )
    ).all()

    advanced_questions = db.exec(
        select(Question).where(
            Question.topic_id == topic_id,
            Question.level == "advanced"
        )
    ).all()

    total_questions = (
        len(beginner_questions)
        +
        len(intermediate_questions)
        +
        len(advanced_questions)
    )

    if total_questions < 10:
        raise Exception(
            "Minimum 10 questions required for test"
        )

    questions = []

    # =====================================
    # BEGINNER TEST
    # 8 Beginner + 2 Intermediate
    # =====================================

    if level == "beginner":

        questions.extend(
            sample(
                beginner_questions,
                min(8, len(beginner_questions))
            )
        )

        questions.extend(
            sample(
                intermediate_questions,
                min(2, len(intermediate_questions))
            )
        )

    # =====================================
    # INTERMEDIATE TEST
    # 6 Intermediate + 4 Beginner
    # =====================================

    elif level == "intermediate":

        questions.extend(
            sample(
                intermediate_questions,
                min(6, len(intermediate_questions))
            )
        )

        questions.extend(
            sample(
                beginner_questions,
                min(4, len(beginner_questions))
            )
        )

    # =====================================
    # ADVANCED TEST
    # 6 Advanced + 3 Intermediate + 1 Beginner
    # =====================================

    elif level == "advanced":

        questions.extend(
            sample(
                advanced_questions,
                min(6, len(advanced_questions))
            )
        )

        questions.extend(
            sample(
                intermediate_questions,
                min(3, len(intermediate_questions))
            )
        )

        questions.extend(
            sample(
                beginner_questions,
                min(1, len(beginner_questions))
            )
        )

    else:
        raise Exception(
            "Invalid level"
        )

    # Shuffle final test
    questions = sample(
        questions,
        len(questions)
    )

    return questions




PASS_PERCENTAGE = {
    "beginner": 60,
    "intermediate": 70,
    "advanced": 80
}


def evaluate_test(
    db: Session,
    user_id: int,
    topic_id: int,
    level: str,
    question_ids,
    answers
):

    # =====================================
    # Maximum Attempts Check
    # =====================================

    attempts = db.exec(
        select(TestAttempt).where(
            TestAttempt.user_id == user_id,
            TestAttempt.topic_id == topic_id
        )
    ).all()

    if len(attempts) >= 3:
        raise Exception(
            "Maximum attempts reached"
        )

    # =====================================
    # Fetch Same Questions Given In Test
    # =====================================

    questions = db.exec(
        select(Question).where(
            Question.id.in_(question_ids)
        )
    ).all()

    if not questions:
        raise Exception(
            "No questions found"
        )

    # =====================================
    # Correct Answer Mapping
    # =====================================

    correct_map = {
        q.id: q.correct_answer
        for q in questions
    }

    score = 0

    for ans in answers:

        if (
            correct_map.get(ans.question_id)
            ==
            ans.selected
        ):
            score += 1

    # =====================================
    # Calculate Result
    # =====================================

    total = len(questions)

    percentage = (
        score / total
    ) * 100

    required_percentage = PASS_PERCENTAGE.get(
        level,
        60
    )

    passed = (
        percentage >= required_percentage
    )

    # =====================================
    # Save Test Attempt
    # =====================================

    attempt = TestAttempt(
        user_id=user_id,
        topic_id=topic_id,
        level=level,
        score=score,
        total=total,
        passed=passed
    )

    db.add(attempt)

    # =====================================
    # Verify Tutor
    # =====================================

    if passed:

        user_skill = db.exec(
            select(UserSkill).where(
                UserSkill.user_id == user_id,
                UserSkill.topic_id == topic_id,
                UserSkill.type == "teach"
            )
        ).first()

        if user_skill:

            user_skill.is_verified = True

            db.add(user_skill)

            tutor_verified_email_task.delay(user.email)

            create_notification(
                db=db,
                user_id=user_id,
                title="Tutor Verified",
                message="Congratulations! You are now a verified tutor.",
                type="verification"
            )

    db.commit()

    return {
        "score": score,
        "total": total,
        "percentage": round(
            percentage,
            2
        ),
        "required_percentage": required_percentage,
        "passed": passed,
        "message": (
            "Tutor Verified Successfully"
            if passed
            else
            "Tutor Verification Failed"
        )
    }