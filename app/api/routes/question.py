from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi import UploadFile, File

from app.services.excel_question_service import (
    upload_questions_from_excel
)
from fastapi.responses import StreamingResponse

from app.services.excel_template_service import (
    generate_question_template
)
from sqlmodel import Session, select

from app.db.session import get_session

from app.api.deps import (
    get_current_user,
    require_admin
)

from app.schemas.question import (
    QuestionCreate,
    QuestionUpdate
)

from app.services.question_service import (
    create_question,
    get_questions,
    get_question_by_id,
    update_question,
    delete_question,
    bulk_save_questions
)
from app.schemas.ai_question import (
    GenerateQuestionRequest,
    SaveGeneratedQuestions
)

from app.services.ai_question_service import (
    generate_questions
)

from app.models.topic import Topic

router = APIRouter(
    prefix="/questions",
    tags=["Question Bank"]
)


# ---------------------------------------
# Create Question
# ---------------------------------------

@router.post("/")
def create_question_api(
    data: QuestionCreate,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):

    try:

        require_admin(current_user)

        return create_question(

    db,

    data,

    current_user.id

)

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------------------------------
# Get Questions
# ---------------------------------------

@router.get("/")
def get_questions_api(

    topic_id: int | None = None,
    topic_name: str | None = None,
    level: str | None = None,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    try:

        require_admin(current_user)

        return get_questions(

            db=db,

            topic_id=topic_id,

            topic_name=topic_name,

            level=level

        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------------------------------
# Get Question By Id
# ---------------------------------------

@router.get("/{question_id}")
def get_question_api(

    question_id: int,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    try:

        require_admin(current_user)

        return get_question_by_id(
            db,
            question_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------------------------------
# Update Question
# ---------------------------------------

@router.put("/{question_id}")
def update_question_api(

    question_id: int,

    data: QuestionUpdate,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    try:

        require_admin(current_user)

        return update_question(
            db,
            question_id,
            data
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------------------------------
# Delete Question
# ---------------------------------------

@router.delete("/{question_id}")
def delete_question_api(

    question_id: int,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    try:

        require_admin(current_user)

        return delete_question(
            db,
            question_id
        )

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )



@router.post("/upload")
def upload_questions(

    file: UploadFile = File(...),

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    require_admin(current_user)

    return upload_questions_from_excel(

        db,

        file,

        current_user.id

    )
@router.get("/template")
def download_question_template():

    stream = generate_question_template()

    return StreamingResponse(

        stream,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={

            "Content-Disposition":
            "attachment; filename=questions_template.xlsx"

        }

    )
# ==========================================
# AI Generate Questions
# ==========================================

@router.post("/generate")
def generate_ai_questions(

    request: GenerateQuestionRequest,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    # ======================================
    # Admin Check
    # ======================================

    if current_user.role != "admin":

        raise HTTPException(

            status_code=403,

            detail="Only admin can generate AI questions."

        )

    # ======================================
    # Validate Request
    # ======================================

    if not request.topic_id and not request.topic_name:

        raise HTTPException(

            status_code=400,

            detail="Provide topic_id or topic_name."

        )

    topic = None

    # ======================================
    # Topic by ID
    # ======================================

    if request.topic_id:

        topic = db.get(

            Topic,

            request.topic_id

        )

    # ======================================
    # Topic by Name
    # ======================================

    elif request.topic_name:

        topic = db.exec(

            select(Topic).where(

                Topic.name.ilike(

                    request.topic_name

                )

            )

        ).first()

    if not topic:

        raise HTTPException(

            status_code=404,

            detail="Topic not found."

        )

    questions = generate_questions(

        topic.id,

        topic.name,

        request.beginner_count,

        request.intermediate_count,

        request.advanced_count

    )

    return {

        "topic": topic.name,

        "total": len(questions),

        "questions": questions

    }
# ==========================================
# Save AI Questions
# ==========================================

@router.post("/save-generated")
def save_generated_questions(

    data: SaveGeneratedQuestions,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    if current_user.role != "admin":

        raise HTTPException(

            status_code=403,

            detail="Only admin can save questions."

        )

    questions = []

    for q in data.questions:

        questions.append({

            "topic_id": q.topic_id,

            "level": q.level,

            "question": q.question,

            "option_a": q.option_a,

            "option_b": q.option_b,

            "option_c": q.option_c,

            "option_d": q.option_d,

            "correct_answer": q.correct_answer.lower(),

            "explanation": q.explanation,

            "source": "ai",

            "created_by": current_user.id

        })

    result = bulk_save_questions(

        db,

        questions

    )

    return {

        "message": "Questions saved successfully.",

        "result": result

    }