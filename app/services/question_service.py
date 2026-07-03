from sqlmodel import Session, select
from typing import Optional
from app.models.question import Question
from app.models.topic import Topic
from fastapi import HTTPException
from app.models.user import User
import random
def create_question(
    db: Session,
    data,
    created_by: int
):

    # =====================================
    # 🔥 Topic Resolution
    # =====================================

    topic_id = data.topic_id

    if data.topic_name:

        topic = db.exec(
            select(Topic).where(
                Topic.name.ilike(
                    data.topic_name
                )
            )
        ).first()

        if not topic:
            raise Exception(
                "Topic not found"
            )

        topic_id = topic.id

    if not topic_id:
        raise Exception(
            "Provide topic_id or topic_name"
        )

    VALID_LEVELS = [
        "beginner",
        "intermediate",
        "advanced"
    ]

    level = data.level.lower()

    if level not in VALID_LEVELS:
        raise Exception(
            "Invalid level"
        )

    answer = data.correct_answer.lower()

    if answer not in [
        "a",
        "b",
        "c",
        "d"
    ]:
        raise Exception(
            "Correct answer must be a,b,c,d"
        )

    # =====================================
    # 🔥 Duplicate Check
    # =====================================

    existing = db.exec(
        select(Question).where(
            Question.topic_id == topic_id,
            Question.question == data.question
        )
    ).first()

    if existing:
        raise Exception(
            "Question already exists"
        )

    # =====================================
    # 🔥 Create Question
    # =====================================

    question = Question(

    topic_id=topic_id,

    level=level,

    question=data.question,

    option_a=data.option_a,

    option_b=data.option_b,

    option_c=data.option_c,

    option_d=data.option_d,

    correct_answer=answer,

    explanation=data.explanation,

    source="manual",

    created_by=created_by

)

    db.add(question)

    db.commit()

    db.refresh(question)

    return question


def is_duplicate_question(

    db: Session,

    topic_id: int,

    question: str

):

    existing = db.exec(

        select(Question).where(

            Question.topic_id == topic_id,

            Question.question == question

        )

    ).first()

    return existing is not None


def save_question(

    db: Session,

    topic_id: int,
    level: str,
    question: str,
    option_a: str,
    option_b: str,
    option_c: str,
    option_d: str,
    correct_answer: str,
    explanation: str | None,
    source: str,
    created_by: int

):

    if is_duplicate_question(

        db,

        topic_id,
        question

    ):

        return None

    obj = Question(

        topic_id=topic_id,

        level=level,

        question=question,

        option_a=option_a,

        option_b=option_b,

        option_c=option_c,

        option_d=option_d,

        correct_answer=correct_answer,

        explanation=explanation,

        source=source,

        created_by=created_by

    )

    db.add(obj)

    return obj


def bulk_save_questions(

    db: Session,

    questions: list

):

    inserted = 0

    duplicate = 0

    for q in questions:

        obj = save_question(

            db,

            topic_id=q["topic_id"],

            level=q["level"],

            question=q["question"],

            option_a=q["option_a"],

            option_b=q["option_b"],

            option_c=q["option_c"],

            option_d=q["option_d"],

            correct_answer=q["correct_answer"],

            explanation=q.get("explanation"),

            source=q["source"],

            created_by=q["created_by"]

        )

        if obj:

            inserted += 1

        else:

            duplicate += 1

    db.commit()

    return {

        "inserted": inserted,

        "duplicates": duplicate

    }


def get_questions(
    db: Session,
    topic_id: Optional[int] = None,
    topic_name: Optional[str] = None,
    level: Optional[str] = None
):

    # =====================================
    # Topic Name Support
    # =====================================

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

    # =====================================
    # Build Query
    # =====================================

    query = select(Question)

    if topic_id:

        query = query.where(
            Question.topic_id == topic_id
        )

    if level:

        query = query.where(
            Question.level == level
        )

    # =====================================
    # Execute Query
    # =====================================

    return db.exec(query).all()

def get_question_by_id(
    db: Session,
    question_id: int
):

    return db.get(
        Question,
        question_id
    )


def update_question(
    db: Session,
    question_id: int,
    data
):

    question = db.get(
        Question,
        question_id
    )

    if not question:
        raise Exception(
            "Question not found"
        )

    updates = data.model_dump(
        exclude_unset=True
    )

    for key, value in updates.items():
        setattr(
            question,
            key,
            value
        )

    db.add(question)

    db.commit()

    db.refresh(question)

    return question


def delete_question(
    db: Session,
    question_id: int
):

    question = db.get(
        Question,
        question_id
    )

    if not question:
        raise Exception(
            "Question not found"
        )

    db.delete(question)

    db.commit()

    return {
        "message": "Question deleted"
    }

# ==========================================
# Random Questions For Verification
# ==========================================

def get_random_questions(

    db: Session,

    topic_id: int | None = None,

    topic_name: str | None = None

):


 if not topic_id and not topic_name:

    raise HTTPException(
        status_code=400,
        detail="Provide topic_id or topic_name."
    )

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
    
    REQUIRED = {

        "beginner": 2,

        "intermediate": 3,

        "advanced": 5

    }

    selected = []

    used_ids = set()

    # --------------------------------------
    # Helper
    # --------------------------------------

    def fetch(level):

        questions = db.exec(

            select(Question).where(

                Question.topic_id == topic_id,

                Question.level == level,

                Question.is_active == True

            )

        ).all()

        random.shuffle(questions)

        return questions

    beginner = fetch("beginner")

    intermediate = fetch("intermediate")

    advanced = fetch("advanced")

    pools = {

        "beginner": beginner,

        "intermediate": intermediate,

        "advanced": advanced

    }

    # --------------------------------------
    # First Pass
    # --------------------------------------

    remaining = {}

    for level, required in REQUIRED.items():

        available = pools[level]

        take = min(required, len(available))

        remaining[level] = required - take

        for q in available[:take]:

            selected.append(q)

            used_ids.add(q.id)

    # --------------------------------------
    # Fallback
    # --------------------------------------

    if remaining["advanced"] > 0:

        extra = [

            q for q in intermediate

            if q.id not in used_ids

        ]

        take = min(

            remaining["advanced"],

            len(extra)

        )

        for q in extra[:take]:

            selected.append(q)

            used_ids.add(q.id)

        remaining["advanced"] -= take

    if remaining["advanced"] > 0:

        extra = [

            q for q in beginner

            if q.id not in used_ids

        ]

        take = min(

            remaining["advanced"],

            len(extra)

        )

        for q in extra[:take]:

            selected.append(q)

            used_ids.add(q.id)

        remaining["advanced"] -= take

    if remaining["intermediate"] > 0:

        extra = [

            q for q in beginner

            if q.id not in used_ids

        ]

        take = min(

            remaining["intermediate"],

            len(extra)

        )

        for q in extra[:take]:

            selected.append(q)

            used_ids.add(q.id)

    # --------------------------------------
    # Final Validation
    # --------------------------------------

    if len(selected) < 10:

        raise HTTPException(

            status_code=400,

            detail="Not enough questions available."

        )

    random.shuffle(selected)

    return selected