from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.accounts import Account
from models.transactions import Transactions


def get_transactions(db: Session, account_id):
    existing = db.query(Transactions).filter(Transactions.user_id == Account.id)
    if not existing:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    query = db.query(Transactions).options(joinedload(Account.id))

    return query.order_by(Transactions.date.desc)
