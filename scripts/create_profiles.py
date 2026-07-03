import sys
from pathlib import Path

from sqlmodel import Session, select

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from app.db.session import engine

from app.models.user import User
from app.models.profile import Profile


with Session(engine) as db:

    users = db.exec(
        select(User)
    ).all()

    for user in users:

        existing = db.exec(
            select(Profile).where(
                Profile.user_id == user.id
            )
        ).first()

        if not existing:

            db.add(
                Profile(
                    user_id=user.id
                )
            )

    db.commit()

print("Profiles created ✅")