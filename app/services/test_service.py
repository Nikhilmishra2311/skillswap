from sqlmodel import Session, select
from app.models.question import Question
from app.models.test_attempt import TestAttempt
from app.models.user_skill import UserSkill


def get_questions(db: Session, topic_id: int, level: str):
    return db.exec(
        select(Question).where(
            Question.topic_id == topic_id,
            Question.level == level
        )
    ).all()


def evaluate_test(db: Session, user_id: int, topic_id: int, level: str, answers):

    questions = get_questions(db, topic_id, level)

    if not questions:
        raise Exception("No questions found for this level")

    correct_map = {q.id: q.correct_answer for q in questions}

    score = 0

    for ans in answers:
       if correct_map.get(ans.question_id) == ans.selected:
            score += 1

    # ✅ FIXED LOGIC
    total = len(questions)
    passed = score >= (total * 0.6)

    attempt = TestAttempt(
        user_id=user_id,
        topic_id=topic_id,
        level=level,
        score=score,
        total=total,
        passed=passed
    )

    db.add(attempt)

    # ✅ Tutor verification
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

    db.commit()

    return {
        "score": score,
        "total": total,
        "passed": passed
    }