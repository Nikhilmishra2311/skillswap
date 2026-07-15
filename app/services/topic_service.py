from sqlmodel import Session
from app.models.topic import Topic
from math import ceil
from sqlmodel import select
from app.services.cache_service import (
    get_cache,
    set_cache,
    delete_cache,
    delete_pattern
)




def create_topic(db: Session, name: str):

    topic = Topic(name=name)

    db.add(topic)
    db.commit()

    # Clear cache
    delete_pattern(
    "topics:*"
)
    db.refresh(topic)
    
    return topic
def get_topics(

    db: Session,

    page: int = 1,

    size: int = 20

):

    cache_key = f"topics:{page}:{size}"

    cached = get_cache(cache_key)

    if cached:

        print("✅ Topics fetched from Redis")

        return cached

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

    response = {

        "page": page,
        "size": size,
        "total": total,
        "total_pages": ceil(total / size) if total else 0,
        "items": topics

    }

    set_cache(
        cache_key,
        response,
        expire=300
    )

    return response