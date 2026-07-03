from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    return pwd_context.verify(
        plain_password[:72],
        hashed_password
    )


def create_access_token(
    data: dict,
    expires_delta: timedelta = None
):
    to_encode = data.copy()

    expire = (
        datetime.utcnow() + expires_delta
        if expires_delta
        else datetime.utcnow()
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = {
        "sub": email,
        "exp": expire
    }

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload.get("sub")

    except JWTError:
        return None