from sqlmodel import Session
from app.models.topic import Topic

def create_topic(db: Session, name: str):
    topic = Topic(name=name)
    
    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic