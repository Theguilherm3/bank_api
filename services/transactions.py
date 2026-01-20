from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.accounts import Account
from models.transactions import Transactions
from schemas.transactions import TransactionCreate


def get_transactions(db: Session, account_id):
    transactions = (
        db.query(Transactions)
        .filter(Transactions.account_id == account_id)
        .order_by(Transactions.date.desc())
        .all()
    )
    if not transactions:
        raise HTTPException(status_code=404, detail="Nenhuma Transação Encontrada")

    return transactions


def create_transacion(db: Session, new_transaction: TransactionCreate):
    check_account: Account | None = (
        db.query(Account)
        .filter(Account.account_number == new_transaction.account_id)
        .first()
    )

    if not check_account:
        raise HTTPException(status_code=404, detail="Conta não encontrada no sistema")

    elif check_account.balance < new_transaction.amount:
        raise HTTPException(status_code=400, detail="Saldo Insuficiente")

    create_new_transacion = Transactions(
        movment_type=new_transaction.movment_type,
        account_id=new_transaction.account_id,
        transaction_type=new_transaction.transaction_type,
        amount=new_transaction.amount,
        date=date.today(),
    )

    db.add(create_new_transacion)
    db.commit()
    db.refresh(create_new_transacion)

    return create_new_transacion
