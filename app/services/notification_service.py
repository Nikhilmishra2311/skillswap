from sqlmodel import Session, select

from app.models.notification import Notification

from math import ceil
def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    type: str
):

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=type
    )

    db.add(notification)
    db.commit()

    db.refresh(notification)

    return notification
def get_notifications(

    db: Session,

    user_id: int,

    page: int = 1,

    size: int = 10

):

    query = (

        select(Notification)

        .where(Notification.user_id == user_id)

        .order_by(Notification.created_at.desc())

    )

    total = len(
        db.exec(query).all()
    )

    offset = (page - 1) * size

    notifications = db.exec(

        query.offset(offset).limit(size)

    ).all()

    return {

        "page": page,
        "size": size,
        "total": total,
        "total_pages": ceil(total / size) if total else 0,
        "items": notifications

    }

def mark_notification_read(
    db: Session,
    notification_id: int,
    user_id: int
):

    notification = db.get(
        Notification,
        notification_id
    )

    if not notification:
        raise Exception(
            "Notification not found"
        )

    if notification.user_id != user_id:
        raise Exception(
            "Unauthorized"
        )

    notification.is_read = True

    db.add(notification)

    db.commit()

    db.refresh(notification)

    return notification