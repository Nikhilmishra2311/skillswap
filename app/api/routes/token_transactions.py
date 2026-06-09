from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user
from app.services.token_transaction_service import get_my_transactions

router = APIRouter(
    prefix="/transactions",
    tags=["Token Transactions"]
)

@router.get("/my")
def my_transactions(
    db: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    return get_my_transactions(
        db,
        current_user.id
    )