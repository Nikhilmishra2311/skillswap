import token
from fastapi import Request

from app.core.limiter import limiter

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.tasks.email_tasks import reset_password_email_task, welcome_email_task
from app.db.session import get_session
from app.schemas.user import (
    UserCreate,
    UserLogin,
    Token,
    ChangePassword,
    ResetPassword
)
from app.services.auth_service import (
    create_user,
    authenticate_user,
    get_user_by_email,
    reset_user_password
)
from app.core.security import (
    create_access_token,
    verify_password,
    get_password_hash,
    create_reset_token,
    verify_reset_token
)
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


# 🔐 Register
@router.post("/register", response_model=Token)
@limiter.limit("3/minute")
def register(

    request: Request,

    user_data: UserCreate,

    db: Session = Depends(get_session)

):

    try:

        user = create_user(
    db,
    user_data.full_name,
    user_data.email,
    user_data.password
)

        # ==========================================
        # Send Welcome Email (Background)
        # ==========================================

        welcome_email_task.delay(
    user.email,
    user.full_name
)

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# 🔐 Login
@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(

    request: Request,

    user_data: UserLogin,

    db: Session = Depends(get_session)

):

    user = authenticate_user(
        db,
        user_data.email,
        user_data.password
    )

    if not user:

        raise HTTPException(
            status_code=400,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# 🔐 Change Password (logged-in)
@router.post("/change-password")
@limiter.limit("5/minute")
def change_password(

    request: Request,

    data: ChangePassword,

    db: Session = Depends(get_session),

    current_user=Depends(get_current_user)

):

    if not verify_password(
        data.old_password,
        current_user.password
    ):

        raise HTTPException(
            status_code=400,
            detail="Incorrect old password"
        )

    current_user.password = get_password_hash(
        data.new_password
    )

    db.add(current_user)

    db.commit()

    return {
        "message": "Password updated successfully"
    }


# 🔑 Forgot Password (generate token)
@router.post("/forgot-password")
@limiter.limit("3/15minutes")
def forgot_password(

    request: Request,

    email: str,

    db: Session = Depends(get_session)

):

    user = get_user_by_email(
        db,
        email
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    token = create_reset_token(email)

    reset_password_email_task.delay(
        email,
        token
    )

    return {
        "message": "Password reset email sent."
    }


# 🔑 Reset Password
@router.post("/reset-password")
@limiter.limit("5/minutes")
def reset_password(
    request: Request,
    data: ResetPassword,
    db: Session = Depends(get_session)
):
    email = verify_reset_token(data.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = reset_user_password(db, email, data.new_password)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Password reset successful"}