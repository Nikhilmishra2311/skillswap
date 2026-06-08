from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.models.topic import Topic

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/topics")
def search_topics(query: str, db: Session = Depends(get_session)):
    results = db.exec(
        select(Topic).where(Topic.name.contains(query))
    ).all()

    return results