from sqlmodel import Session
from app.models.topic import Topic
from math import ceil
from sqlmodel import select
def create_topic(db: Session, name: str):

    topic = Topic(name=name)
    
    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic
def get_topics(

    db: Session,

    page: int = 1,

    size: int = 20

):

    query = (

        select(Topic)

        .order_by(Topic.name)

    )

    total = len(
        db.exec(query).all()
    )

    offset = (page - 1) * size

    topics = db.exec(

        query.offset(offset).limit(size)

    ).all()

    return {

        "page": page,
        "size": size,
        "total": total,
        "total_pages": ceil(total / size) if total else 0,
        "items": topics

    }