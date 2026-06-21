from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.schemas.question import QuestionPublic
from app.schemas.test import SubmitTest

from app.db.session import get_session
from app.api.deps import get_current_user

from app.services.test_service import (
    get_questions,
    evaluate_test
)

from app.models.user_skill import UserSkill
from app.models.topic import Topic

router = APIRouter(
    prefix="/test",
    tags=["Test"]
)


# 🔥 GET QUESTIONS (Tutor only)
@router.get("/questions", response_model=List[QuestionPublic])
def fetch_questions(
    topic_id: int | None = None,
    topic_name: str | None = None,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    # Must provide one
    if not topic_id and not topic_name:
        raise HTTPException(
            status_code=400,
            detail="Provide topic_id or topic_name"
        )

    # Find topic by name
    if topic_name:

        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(topic_name)
            )
        ).first()

        if not topic:
            raise HTTPException(
                status_code=404,
                detail="Topic not found"
            )

        topic_id = topic.id

    # Tutor check
    user_skill = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == current_user.id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach"
        )
    ).first()

    if not user_skill:
        raise HTTPException(
            status_code=403,
            detail="You are not registered as tutor for this topic"
        )

    level = user_skill.level

    questions = get_questions(
        db,
        topic_id,
        level
    )

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found"
        )

    return questions


# 🔥 SUBMIT TEST
@router.post("/submit")
def submit_test(
    data: SubmitTest,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    # Tutor check
    user_skill = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == current_user.id,
            UserSkill.topic_id == data.topic_id,
            UserSkill.type == "teach"
        )
    ).first()

    if not user_skill:
        raise HTTPException(
            status_code=403,
            detail="You are not registered as tutor for this topic"
        )

    # Prevent retake
    if user_skill.is_verified:
        raise HTTPException(
            status_code=400,
            detail="You are already a verified tutor"
        )

    # Validate answers
    if not data.answers:
        raise HTTPException(
            status_code=400,
            detail="Answers cannot be empty"
        )

    level = user_skill.level

    result = evaluate_test(
        db,
        current_user.id,
        data.topic_id,
        level,
        data.answers
    )

    return {
        "message": "Test submitted successfully",
        "result": result
    }