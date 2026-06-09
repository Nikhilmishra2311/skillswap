from sqlmodel import Session, select
from app.models.token_transaction import TokenTransaction


def get_my_transactions(db: Session, user_id: int):
    transactions = db.exec(
        select(TokenTransaction).where(
            (TokenTransaction.sender_id == user_id)
            | (TokenTransaction.receiver_id == user_id)
        )
    ).all()

    return transactions