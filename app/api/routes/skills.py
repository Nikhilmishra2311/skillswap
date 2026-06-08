from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.db.session import get_session
from app.schemas.skill import SkillCreate
from app.services.skill_service import create_skill

router = APIRouter(prefix="/skills", tags=["Skills"])


@router.post("/")
def create(skill: SkillCreate, db: Session = Depends(get_session)):
    return create_skill(db, skill.name)