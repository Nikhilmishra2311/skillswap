from fastapi import APIRouter, Depends
from sqlmodel import Session
from fastapi import Request
from app.core.limiter import limiter
from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.token_transaction_service import get_my_transactions

router = APIRouter(
    prefix="/transactions",
    tags=["Token Transactions"]
)

@router.get("/my")
@limiter.limit("60/minute")
def my_transactions(
    request: Request,
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    return get_my_transactions(
        db,
        current_user.id
    )