from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

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
def register(user_data: UserCreate, db: Session = Depends(get_session)):
    try:
        user = create_user(db, user_data.email, user_data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# 🔐 Login
@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_session)):
    user = authenticate_user(db, user_data.email, user_data.password)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


# 🔐 Change Password (logged-in)
@router.post("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    if not verify_password(data.old_password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect old password")

    current_user.password = get_password_hash(data.new_password)

    db.add(current_user)
    db.commit()

    return {"message": "Password updated successfully"}


# 🔑 Forgot Password (generate token)
@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_session)):
    user = get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(email)

    # In production → send email
    return {"reset_token": token}


# 🔑 Reset Password
@router.post("/reset-password")
def reset_password(data: ResetPassword, db: Session = Depends(get_session)):
    email = verify_reset_token(data.token)

    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = reset_user_password(db, email, data.new_password)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Password reset successful"}