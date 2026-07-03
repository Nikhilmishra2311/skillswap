from datetime import datetime, timedelta

from sqlmodel import Session, select
from app.tasks.email_tasks import (
    session_reminder_email_task
)
from app.db.session import engine

from app.models.session import Session as LearningSession
from app.models.topic import Topic
from app.models.user import User

from app.tasks.celery_app import celery

from app.tasks.notification_tasks import send_notification_task


# ==========================================
# Expire Old Sessions
# ==========================================

@celery.task
def expire_sessions():

    with Session(engine) as db:

        now = datetime.utcnow()

        sessions = db.exec(

            select(LearningSession).where(

                LearningSession.status == "open",

                LearningSession.start_time < now

            )

        ).all()

        count = 0

        for session in sessions:

            session.status = "expired"

            db.add(session)

            count += 1

        db.commit()

        return f"{count} sessions expired."
    



# ==========================================
# Session Reminder
# ==========================================

@celery.task
def send_session_reminders():

    with Session(engine) as db:

        now = datetime.utcnow()

        after_30 = now + timedelta(minutes=30)

        sessions = db.exec(

            select(LearningSession).where(

                LearningSession.status == "booked",

                LearningSession.start_time >= now,

                LearningSession.start_time <= after_30

            )

        ).all()

        for session in sessions:

            if session.tutor_id:

                send_notification_task.delay(

                    session.tutor_id,

                    "Upcoming Session",

                    "Your session starts in 30 minutes.",

                    "reminder"

                )

                tutor = db.get(User, session.tutor_id)
                topic = db.get(Topic, session.topic_id)
                formatted_time = session.start_time.strftime(
                    "%d %b %Y %I:%M %p"
                )

                if tutor and topic:
                    session_reminder_email_task.delay(
                        tutor.email,
                        tutor.full_name,
                        topic.name,
                        formatted_time
                    )

            if session.learner_id:

                send_notification_task.delay(

                    session.learner_id,

                    "Upcoming Session",

                    "Your session starts in 30 minutes.",

                    "reminder"

                )

                learner = db.get(User, session.learner_id)
                topic = db.get(Topic, session.topic_id)
                formatted_time = session.start_time.strftime(
                    "%d %b %Y %I:%M %p"
                )

                if learner and topic:
                    session_reminder_email_task.delay(
                        learner.email,
                        learner.full_name,
                        topic.name,
                        formatted_time
                    )

        return f"{len(sessions)} reminders queued."
    

# ==========================================
# Cleanup Expired Sessions
# ==========================================

@celery.task
def cleanup_old_sessions():

    with Session(engine) as db:

        threshold = datetime.utcnow() - timedelta(days=30)

        sessions = db.exec(

            select(LearningSession).where(

                LearningSession.status == "expired",

                LearningSession.start_time < threshold

            )

        ).all()

        deleted = 0

        for session in sessions:

            db.delete(session)

            deleted += 1

        db.commit()

        return f"{deleted} sessions deleted."