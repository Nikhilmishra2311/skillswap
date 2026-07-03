import sys
from pathlib import Path

from sqlmodel import Session, select

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.db.session import engine
from app.models.user import User


EMAIL = "mishranikhil2311@gmail.com"


with Session(engine) as db:

    user = db.exec(
        select(User).where(
            User.email == EMAIL
        )
    ).first()

    if not user:
        print("User not found")
        exit()

    user.role = "admin"

    db.add(user)

    db.commit()

print("Admin created ✅")