from app.tasks.celery_app import celery
from sqlmodel import Session
from app.db.session import engine
from app.services.notification_service import create_notification


@celery.task(bind=True, max_retries=3)
def send_notification_task(
    self,
    user_id: int,
    title: str,
    message: str,
    notification_type: str
):
    try:
        with Session(engine) as db:

            create_notification(
                db=db,
                user_id=user_id,
                title=title,
                message=message,
                type=notification_type
            )

            return "Notification Created"

    except Exception as e:
        raise self.retry(exc=e, countdown=5)