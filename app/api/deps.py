from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlmodel import Session, select
from app.core.config import settings
from app.db.session import get_session
from app.models.user import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_session)
):
    token = credentials.credentials  # Extract token

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.exec(select(User).where(User.id == int(user_id))).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

def require_admin(current_user):

    if current_user.role != "admin":

        raise HTTPException(
            status_code=403,
            detail="Only admin can perform this action."
        )

    return current_user
