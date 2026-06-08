from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.schemas.topic import TopicCreate
from app.services.topic_service import create_topic
from app.models.topic import Topic   # 🔥 IMPORTANT

router = APIRouter(prefix="/topics", tags=["Topics"])


# 🔥 Create topic
@router.post("/")
def create(topic: TopicCreate, db: Session = Depends(get_session)):
    return create_topic(db, topic.name)


# 🔥 Get all topics
@router.get("/")   # ✅ FIXED
def get_topics(db: Session = Depends(get_session)):
    return db.exec(select(Topic)).all()