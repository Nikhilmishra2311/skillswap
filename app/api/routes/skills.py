from urllib.request import Request
from fastapi import Request
from fastapi import APIRouter, Depends
from app.core.limiter import limiter
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.skill import SkillCreate
from app.services.skill_service import create_skill

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("/")
@limiter.limit("20/minute")
def create(request: Request, skill: SkillCreate, db: Session = Depends(get_session)):
    return create_skill(db, skill.name)