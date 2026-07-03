import re

from sqlmodel import Session, select

from app.models.profile import Profile
from app.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str):
    return db.exec(select(User).where(User.email == email)).first()


def generate_username(db: Session, full_name: str):
    base_username = re.sub(r'[^a-zA-Z0-9]', '', full_name.lower())

    username = base_username

    count = 1

    while db.exec(select(User).where(User.username == username)).first():
        username = f"{base_username}{count}"
        count += 1

    return username


def create_user(
    db: Session,
    full_name: str,
    email: str,
    password: str
):
    if get_user_by_email(db, email):
        raise ValueError("Email already registered")

    hashed_password = get_password_hash(password)

    username = generate_username(db, full_name)

    role = "user"

    if email.lower() == settings.SUPER_ADMIN_EMAIL.lower():
        role = "admin"

    user = User(
        full_name=full_name,
        username=username,
        email=email,
        password=hashed_password,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    profile = Profile(user_id=user.id)

    db.add(profile)
    db.commit()

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