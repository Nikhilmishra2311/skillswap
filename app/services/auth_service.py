from sqlmodel import Session, select
from app.models.user import User
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()


def create_user(db: Session, email: str, password: str):
    # Check duplicate email
    if get_user_by_email(db, email):
        raise ValueError("Email already registered")

    hashed_password = get_password_hash(password)

    user = User(
        email=email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user
def reset_user_password(db: Session, email: str, new_password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    user.password = get_password_hash(new_password)

    db.add(user)
    db.commit()

    return user