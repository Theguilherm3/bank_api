import random

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from models.accounts import Account
from models.transactions import EnumMovmentType, EnumPaymentTypes
from schemas.accounts import AccountCreate
from schemas.transactions import TransactionCreate
from services.transactions import create_transacion


def get_balance(db: Session, account_number):
    existing = (
        db.query(Account).filter(Account.account_number == account_number).first()
    )

    if not existing:
        raise HTTPException(status_code=404, detail="Account not found")

    query = (
        db.query(Account)
        .options(joinedload(Account.transactions))
        .filter(Account.account_number == account_number)
    )
    print(query)

    return query.first()


def create_account(db: Session, new_account: AccountCreate):
    existing = (
        db.query(Account).filter(Account.username == new_account.username).first()
    )

    if existing:
        raise HTTPException(status_code=409, detail="Conta com esse nome já existe")

    create_new_account = Account(
        username=new_account.username, account_number=random.randint(1000, 9999)
    )

    create_initial_balance = TransactionCreate(
        movment_type=EnumMovmentType.ENTRADA,
        transaction_type=EnumPaymentTypes.P,
        account_id=create_new_account.account_number,
        amount=new_account.balance,
    )

    db.add(create_new_account)
    db.commit()
    db.refresh(create_new_account)
    create_transacion(db, create_initial_balance)

    return create_new_account
