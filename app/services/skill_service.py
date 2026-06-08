from sqlmodel import Session
from app.models.skill import Skill

def create_skill(db: Session, name: str):
    skill = Skill(name=name)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill