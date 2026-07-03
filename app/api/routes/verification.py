from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.session import get_session

from app.api.deps import get_current_user

from app.schemas.verification import (
    StartVerificationRequest,
    SubmitVerificationRequest
)

from app.services.verification_service import (

    get_user_skill,

    start_verification,

    submit_verification

)

router = APIRouter(
    prefix="/verification",
    tags=["Tutor Verification"]
)


# ==========================================
# Start Verification Test
# ==========================================

@router.post("/start")
def start_verification_api(

    data: StartVerificationRequest,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    try:

        user_skill = get_user_skill(

            db=db,

            user_id=current_user.id,

            topic_id=data.topic_id,

            topic_name=data.topic_name

        )

        attempt, questions = start_verification(

            db=db,

            user=current_user,

            user_skill=user_skill

        )

        response_questions = []

        for q in questions:

            response_questions.append({

                "id": q.id,

                "question": q.question,

                "option_a": q.option_a,

                "option_b": q.option_b,

                "option_c": q.option_c,

                "option_d": q.option_d

            })

        return {

            "attempt_id": attempt.id,

            "duration": 20,

            "expires_at": attempt.expires_at,

            "questions": response_questions

        }

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )


# ==========================================
# Submit Verification
# ==========================================

@router.post("/submit")
def submit_verification_api(

    data: SubmitVerificationRequest,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    try:

        result = submit_verification(

            db=db,

            attempt_id=data.attempt_id,

            answers=data.answers

        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )