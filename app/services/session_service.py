from sqlmodel import Session as DBSession, select
from sqlalchemy import or_
from app.models.session import Session
from app.models.user import User
from app.models.token_transaction import TokenTransaction
from app.models.user_skill import UserSkill
from app.models.topic import Topic 
from datetime import datetime, timedelta
from app.models.availability import AvailabilitySlot
from app.tasks.notification_tasks import send_notification_task
from app.tasks.email_tasks import (
    session_booked_email_task,
    session_completed_email_task,
    session_reminder_email_task
)
from app.services.cache_service import (
    get_cache,
    set_cache,
    delete_cache,
    delete_pattern
)

from app.core.cache import redis_client
from app.services.jitsi_service import generate_meeting

from math import ceil

TOKEN_PER_SESSION = 10


def create_session(
    db: DBSession,
    tutor_id: int,
    topic_id: int,
    start_time
):

    # =====================================
    # Cannot create session in past
    # =====================================

    now = datetime.now()

    if start_time <= now:
        raise Exception("Start time must be in the future.")

    # =====================================
    # Availability Validation
    # =====================================

    session_day = start_time.strftime("%A")
    session_time = start_time.strftime("%H:%M")

    availability_slots = db.exec(
        select(AvailabilitySlot).where(
            AvailabilitySlot.user_id == tutor_id,
            AvailabilitySlot.day == session_day,
            AvailabilitySlot.is_active == True
        )
    ).all()

    if not availability_slots:
        raise Exception(
            f"No availability found for {session_day}"
        )

    requested_time = datetime.strptime(
        session_time,
        "%H:%M"
    ).time()

    selected_slot = None

    for slot in availability_slots:
        slot_start = datetime.strptime(
            slot.start_time,
            "%H:%M"
        ).time()

        slot_end = datetime.strptime(
            slot.end_time,
            "%H:%M"
        ).time()

        if slot_start <= requested_time <= slot_end:
            selected_slot = slot
            break

    if not selected_slot:
        raise Exception(
            "You are not available at this time."
        )

    # =====================================
    # Tutor Verification
    # =====================================

    user_skill = db.exec(
        select(UserSkill).where(
            UserSkill.user_id == tutor_id,
            UserSkill.topic_id == topic_id,
            UserSkill.type == "teach",
            UserSkill.is_verified == True
        )
    ).first()

    if not user_skill:
        raise Exception(
            "Only verified tutors can create sessions."
        )

    # =====================================
    # Active Session Validation
    # =====================================

    existing = db.exec(
        select(Session).where(
            Session.tutor_id == tutor_id,
            Session.status.in_(
                [
                    "open",
                    "booked",
                    "ongoing"
                ]
            )
        )
    ).first()

    if existing:
        raise Exception(
            "You already have an active session."
        )

    # =====================================
    # Create Session
    # =====================================

    session = Session(
        tutor_id=tutor_id,
        topic_id=topic_id,
        availability_slot_id=selected_slot.id,
        start_time=start_time,
        status="open"
    )

    db.add(session)

    db.commit()
    delete_pattern(
    "available_sessions:*"
         )

    db.refresh(session)

    
    send_notification_task.delay(
        tutor_id,
        "Session Created",
        "Your session is now visible to learners.",
        "session_created"
    )

    return session




def get_available_sessions(

    db: DBSession,

    topic_id: int | None = None,

    topic_name: str | None = None,

    page: int = 1,

    size: int = 10

):

    # =====================================
    # Cache Key
    # =====================================

    cache_key = (
        f"available_sessions:"
        f"{topic_id}:"
        f"{topic_name}:"
        f"{page}:"
        f"{size}"
    )

    cached = get_cache(cache_key)

    if cached:

        print("✅ Available Sessions fetched from Redis")

        return cached

    # =====================================
    # Auto Expire Old Sessions
    # =====================================

    now = datetime.now()

    open_sessions = db.exec(
        select(Session).where(
            Session.status == "open"
        )
    ).all()

    updated = False

    for item in open_sessions:

        if item.start_time <= now:

            item.status = "expired"

            db.add(item)

            updated = True

    if updated:
        db.commit()

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

            response = {
                "page": page,
                "size": size,
                "total": 0,
                "total_pages": 0,
                "items": []
            }

            set_cache(
                cache_key,
                response,
                expire=120
            )

            return response

        topic_id = topic.id

    # =====================================
    # Fetch Sessions
    # =====================================

    query = select(Session).where(

        Session.status == "open",

        Session.start_time > now

    )

    if topic_id:

        query = query.where(
            Session.topic_id == topic_id
        )

    query = query.order_by(
        Session.start_time
    )

    total = len(
        db.exec(query).all()
    )

    offset = (page - 1) * size

    sessions = db.exec(
        query.offset(offset).limit(size)
    ).all()

    result = []

    for session in sessions:

        tutor = db.get(
            User,
            session.tutor_id
        )

        topic = db.get(
            Topic,
            session.topic_id
        )

        result.append({

            "session_id": session.id,

            "topic_id": topic.id if topic else None,

            "topic_name": topic.name if topic else None,

            "tutor_id": tutor.id if tutor else None,

            "tutor_email": tutor.email if tutor else None,

            "status": session.status,

            "start_time": session.start_time

        })

    response = {

        "page": page,

        "size": size,

        "total": total,

        "total_pages": ceil(total / size) if total else 0,

        "items": result

    }

    # =====================================
    # Save Cache
    # =====================================

    set_cache(

        cache_key,

        response,

        expire=120

    )

    return response

def book_session(
    db: DBSession,
    session_id: int,
    learner_id: int
):

    # =====================================
    # Fetch Session
    # =====================================

    session = db.get(
        Session,
        session_id
    )

    if not session:
        raise Exception(
            "Session not found."
        )

    # =====================================
    # Session Validation
    # =====================================

    if session.status != "open":
        raise Exception(
            "Session is no longer available."
        )

    if session.tutor_id == learner_id:
        raise Exception(
            "You cannot book your own session."
        )

    # =====================================
    # Learner Active Session Validation
    # =====================================

    active_session = db.exec(
        select(Session).where(
            Session.learner_id == learner_id,
            Session.status.in_(
                [
                    "booked",
                    "ongoing"
                ]
            )
        )
    ).first()

    if active_session:
        raise Exception(
            "You already have an active session."
        )

    # =====================================
    # Book Session
    # =====================================

    session.learner_id = learner_id

    session.status = "booked"
           # =====================================
           # Generate Meeting
           # =====================================

    meeting_details = generate_meeting(
        session_id=session.id,
        tutor_id=session.tutor_id,
        learner_id=learner_id
    )
    session.meeting_room_id = meeting_details.room_id
    session.meeting_room = meeting_details.room_name
    session.meeting_link = meeting_details.meeting_link

    db.add(session)

    db.commit()
    delete_pattern(
    "available_sessions:*"
         )
    db.refresh(session)

    # =====================================
    # Notifications
    # =====================================

    send_notification_task.delay(
        session.tutor_id,
        "New Session Booked",
        "A learner has booked your session.",
        "booking"
    )

    send_notification_task.delay(
        learner_id,
        "Session Booked",
        "Your session has been booked successfully.",
        "booking"
    )

    tutor = db.get(User, session.tutor_id)
    learner = db.get(User, learner_id)
    topic = db.get(Topic, session.topic_id)

    formatted_time = session.start_time.strftime(
        "%d %b %Y %I:%M %p"
    )

    if tutor and topic:
        session_booked_email_task.delay(
            tutor.email,
            tutor.full_name,
            learner.full_name,
            topic.name,
            formatted_time,
            session.meeting_link
        )

    if learner and topic:
        session_booked_email_task.delay(
            learner.email,
            learner.full_name,
            tutor.full_name,
            topic.name,
            formatted_time,
            session.meeting_link
        )

    if tutor and topic:
        session_reminder_email_task.delay(
            tutor.email,
            tutor.full_name,
            topic.name,
            formatted_time,
            session.meeting_link
        )

   

    return {
    "message": "Session booked successfully.",
    "session_id": session.id,
    "meeting_link": session.meeting_link,
    "meeting_room": session.meeting_room
}


def start_session(
    db: DBSession,
    session_id: int,
    user_id: int
):

    session = db.get(
        Session,
        session_id
    )

    if not session:
        raise Exception(
            "Session not found."
        )

    if session.tutor_id != user_id:
        raise Exception(
            "Only the tutor can start this session."
        )

    if session.status != "booked":
        raise Exception(
            "Session is not ready to start."
        )

    now = datetime.now()

    print("NOW :", now)
    print("SESSION :", session.start_time)

    if now < session.start_time:
        raise Exception(
            "You cannot start the session before its scheduled time."
        )

    if not session.meeting_link:
        raise Exception(
            "Meeting link not found."
        )

    session.status = "ongoing"

    db.add(session)

    db.commit()
    delete_pattern(
    "available_sessions:*"
            )
    db.refresh(session)

    send_notification_task.delay(
        session.learner_id,
        "Session Started",
        "Your tutor has started the session.",
        "session_started"
    )

    send_notification_task.delay(
        session.tutor_id,
        "Session Started",
        "Your session has started successfully.",
        "session_started"
    )

    return {
        "message": "Session Started",
        "meeting_link": session.meeting_link,
        "room_name": session.meeting_room,
        "room_id": session.meeting_room_id
    }

def complete_session(
    db: DBSession,
    session_id: int,
    tutor_id: int
):

    # =====================================
    # Fetch Session
    # =====================================

    session = db.get(
        Session,
        session_id
    )

    if not session:
        raise Exception(
            "Session not found."
        )

    # =====================================
    # Authorization
    # =====================================

    if session.tutor_id != tutor_id:
        raise Exception(
            "Only the tutor can complete this session."
        )

    # =====================================
    # Status Validation
    # =====================================

    if session.status != "ongoing":
        raise Exception(
            "Session must be ongoing."
        )

    if session.learner_id is None:
        raise Exception(
            "No learner booked this session."
        )

    # =====================================
    # Fetch Users
    # =====================================

    tutor = db.get(
        User,
        session.tutor_id
    )

    learner = db.get(
        User,
        session.learner_id
    )

    if not tutor or not learner:
        raise Exception(
            "User not found."
        )

    # =====================================
    # Token Validation
    # =====================================

    SESSION_COST = TOKEN_PER_SESSION

    if learner.token_balance < SESSION_COST:
        raise Exception(
            "Learner has insufficient tokens."
        )

    # =====================================
    # Token Transfer
    # =====================================

    learner.token_balance -= SESSION_COST

    tutor.token_balance += SESSION_COST

    # =====================================
    # Transaction Record
    # =====================================

    transaction = TokenTransaction(
        sender_id=learner.id,
        receiver_id=tutor.id,
        session_id=session.id,
        amount=SESSION_COST
    )

    db.add(transaction)

    # =====================================
    # Complete Session
    # =====================================

    session.status = "completed"
    session.meeting_link=None

    session.meeting_room=None

    session.meeting_room_id=None

    db.add(session)
    db.add(learner)
    db.add(tutor)

    # =====================================
    # Commit Database Changes First
    # =====================================

    db.commit()
    delete_pattern("available_sessions:*")
    db.refresh(session)
    db.refresh(learner)
    db.refresh(tutor)

    # =====================================
    # Tutor Notifications
    # =====================================

    send_notification_task.delay(
        tutor.id,
        "Session Completed",
        "Your teaching session has been completed successfully.",
        "session_completed"
    )

    send_notification_task.delay(
        tutor.id,
        "Tokens Received",
        f"You received {SESSION_COST} tokens.",
        "token"
    )

    # =====================================
    # Learner Notifications
    # =====================================

    send_notification_task.delay(
        learner.id,
        "Session Completed",
        "Your learning session has been completed successfully.",
        "session_completed"
    )

    send_notification_task.delay(
        learner.id,
        "Tokens Deducted",
        f"{SESSION_COST} tokens have been deducted.",
        "token"
    )

    # =====================================
    # Emails
    # =====================================

    topic = db.get(Topic, session.topic_id)

    if tutor and topic:
        session_completed_email_task.delay(
            tutor.email,
            tutor.full_name,
            topic.name,
            SESSION_COST
        )

    if learner and topic:
        session_completed_email_task.delay(
            learner.email,
            learner.full_name,
            topic.name,
            0
        )

    # =====================================
    # Response
    # =====================================

    return {
        "message": "Session completed successfully.",
        "session_id": session.id,
        "tokens_transferred": SESSION_COST,
        "learner_balance": learner.token_balance,
        "tutor_balance": tutor.token_balance
    }


def cancel_session(
    db: DBSession,
    session_id: int,
    user_id: int
):

    # =====================================
    # Fetch Session
    # =====================================

    session = db.get(
        Session,
        session_id
    )

    if not session:
        raise Exception(
            "Session not found."
        )

    # =====================================
    # Authorization
    # =====================================

    if session.tutor_id != user_id:
        raise Exception(
            "Only the tutor can cancel this session."
        )

    # =====================================
    # Status Validation
    # =====================================

    if session.status == "completed":
        raise Exception(
            "Completed session cannot be cancelled."
        )

    if session.status == "cancelled":
        raise Exception(
            "Session is already cancelled."
        )

    if session.status == "expired":
        raise Exception(
            "Expired session cannot be cancelled."
        )

    # =====================================
    # Update Status
    # =====================================

    session.status = "cancelled"
    session.meeting_link=None

    session.meeting_room=None

    session.meeting_room_id=None

    db.add(session)

    # =====================================
    # Save Changes
    # =====================================

    db.commit()
    delete_pattern("available_sessions:*")

    db.refresh(session)

    # =====================================
    # Fetch Users
    # =====================================

    tutor = db.get(
        User,
        session.tutor_id
    )

    learner = None

    if session.learner_id:

        learner = db.get(
            User,
            session.learner_id
        )

    # =====================================
    # Notifications
    # =====================================

    send_notification_task.delay(
        tutor.id,
        "Session Cancelled",
        "You cancelled your session.",
        "session_cancelled"
    )

    if learner:

        send_notification_task.delay(
            learner.id,
            "Session Cancelled",
            "Your tutor cancelled the session.",
            "session_cancelled"
        )

    # =====================================
    # Emails
    # =====================================

    # We will integrate these after
    # creating cancel_session_email_task

    return {

        "message": "Session cancelled successfully.",

        "session_id": session.id,

        "status": session.status

    }
def get_my_created_sessions(

    db: DBSession,

    tutor_id: int,

    page: int = 1,

    size: int = 10

):

    query = (

        select(Session)

        .where(Session.tutor_id == tutor_id)

        .order_by(Session.start_time.desc())

    )

    total = len(
        db.exec(query).all()
    )

    offset = (page - 1) * size

    sessions = db.exec(
        query.offset(offset).limit(size)
    ).all()

    result = []

    for session in sessions:

        learner = None

        if session.learner_id:
            learner = db.get(User, session.learner_id)

        topic = db.get(Topic, session.topic_id)

        result.append({

            "session_id": session.id,
            "topic": topic.name if topic else None,
            "learner_id": learner.id if learner else None,
            "learner_email": learner.email if learner else None,
            "status": session.status,
            "start_time": session.start_time

        })

    return {

        "page": page,
        "size": size,
        "total": total,
        "total_pages": ceil(total / size) if total else 0,
        "items": result

    }
def get_my_booked_sessions(

    db: DBSession,

    learner_id: int,

    page: int = 1,

    size: int = 10

):

    query = (

        select(Session)

        .where(Session.learner_id == learner_id)

        .order_by(Session.start_time.desc())

    )

    total = len(
        db.exec(query).all()
    )

    offset = (page - 1) * size

    sessions = db.exec(
        query.offset(offset).limit(size)
    ).all()

    result = []

    for session in sessions:

        tutor = db.get(User, session.tutor_id)

        topic = db.get(Topic, session.topic_id)

        result.append({

            "session_id": session.id,
            "topic": topic.name if topic else None,
            "tutor_id": tutor.id if tutor else None,
            "tutor_email": tutor.email if tutor else None,
            "status": session.status,
            "start_time": session.start_time

        })

    return {

        "page": page,
        "size": size,
        "total": total,
        "total_pages": ceil(total / size) if total else 0,
        "items": result

    }
def get_session_history(

    db: DBSession,

    user_id: int,

    page: int = 1,

    size: int = 10

):

    query = (

        select(Session)

        .where(

            or_(

                Session.tutor_id == user_id,

                Session.learner_id == user_id

            )

        )

        .order_by(Session.start_time.desc())

    )

    total = len(
        db.exec(query).all()
    )

    offset = (page - 1) * size

    sessions = db.exec(
        query.offset(offset).limit(size)
    ).all()

    result = []

    for session in sessions:

        tutor = db.get(User, session.tutor_id)

        learner = None

        if session.learner_id:
            learner = db.get(User, session.learner_id)

        topic = db.get(Topic, session.topic_id)

        result.append({

            "session_id": session.id,
            "topic": topic.name if topic else None,
            "tutor_email": tutor.email if tutor else None,
            "learner_email": learner.email if learner else None,
            "status": session.status,
            "start_time": session.start_time

        })

    return {

        "page": page,
        "size": size,
        "total": total,
        "total_pages": ceil(total / size) if total else 0,
        "items": result

    }
def get_session_details(
    db: DBSession,
    session_id: int
):

    session = db.get(
        Session,
        session_id
    )

    if not session:

        raise Exception(
            "Session not found."
        )

    tutor = db.get(
        User,
        session.tutor_id
    )

    learner = None

    if session.learner_id:

        learner = db.get(
            User,
            session.learner_id
        )

    topic = db.get(
        Topic,
        session.topic_id
    )

    return {

        "session_id": session.id,

        "topic":
        topic.name if topic else None,

        "tutor": {

            "id":
            tutor.id,

            "email":
            tutor.email

        },

        "learner":

        {

            "id":
            learner.id,

            "email":
            learner.email

        }

        if learner

        else None,

        "status":
        session.status,

        "start_time":
        session.start_time

    }

from datetime import datetime


def get_meeting(
    db: DBSession,
    session_id: int,
    user_id: int
):

    session = db.get(Session, session_id)

    if not session:
        raise Exception("Session not found.")

    # Only tutor or learner

    if user_id not in [
        session.tutor_id,
        session.learner_id
    ]:
        raise Exception(
            "You are not allowed to join this meeting."
        )

    if session.status not in [
        "booked",
        "ongoing"
    ]:
        raise Exception(
            "Meeting is not available."
        )

    if not session.meeting_link:
        raise Exception(
            "Meeting has not been generated."
        )

    # Availability Validation

    slot = db.get(
        AvailabilitySlot,
        session.availability_slot_id
    )

    if slot:

        end_datetime = datetime.combine(
            session.start_time.date(),
            datetime.strptime(
                slot.end_time,
                "%H:%M"
            ).time()
        )

        if datetime.now() > end_datetime:

            raise Exception(
                "Meeting link has expired."
            )

    return {

        "session_id": session.id,

        "room_id": session.meeting_room_id,

        "room_name": session.meeting_room,

        "meeting_link": session.meeting_link,

        "status": session.status
    }


def join_session(

    db: DBSession,

    session_id: int,

    user_id: int

):

    # =====================================
    # Fetch Session
    # =====================================

    session = db.get(Session, session_id)

    if not session:
        raise Exception(
            "Session not found."
        )

    # =====================================
    # Authorization
    # =====================================

    if user_id not in [
        session.tutor_id,
        session.learner_id
    ]:
        raise Exception(
            "You are not allowed to join this session."
        )

    # =====================================
    # Status Validation
    # =====================================

    if session.status not in [
        "booked",
        "ongoing"
    ]:
        raise Exception(
            "Session cannot be joined."
        )

    # =====================================
    # Join Window
    # Allow joining only
    # 10 min before session
    # =====================================

    now = datetime.utcnow()

    join_time = session.start_time - timedelta(
        minutes=10
    )

    if now < join_time:

        remaining = int(
            (join_time - now).total_seconds() // 60
        )

        raise Exception(
            f"You can join only 10 minutes before the session starts. "
            f"Please wait {remaining} minute(s)."
        )

    # =====================================
    # Auto Expire
    # 2 hours after start
    # =====================================

    expire_time = session.start_time + timedelta(
        hours=2
    )

    if now >= expire_time:

        session.status = "expired"

        db.add(session)

        db.commit()


        raise Exception(
            "This session has expired."
        )

    # =====================================
    # Mark Ongoing
    # =====================================

    if session.status == "booked":

        session.status = "ongoing"

        db.add(session)

        db.commit()
        delete_pattern("available_sessions:*")

        db.refresh(session)

    # =====================================
    # Response
    # =====================================

    return {

        "message": "Join session successfully.",

        "session_id": session.id,

        "meeting_room": session.meeting_room,

        "meeting_link": session.meeting_link,

        "status": session.status,

        "starts_at": session.start_time

    }