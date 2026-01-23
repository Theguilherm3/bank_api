from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.session import get_db
from models.accounts import Account
from schemas.transactions import (
    TransacionAllOut,
    TransactionCreate,
    TransactionOut,
    TransferRequest,
)
from services.transactions import create_transacion, get_transactions, transfer_amount

router = APIRouter()


@router.post("/transacao", response_model=TransactionOut, status_code=200)
def create_new_transaction(payload: TransactionCreate, db=Depends(get_db)):
    return create_transacion(db, payload)


@router.get("/transacao/all", response_model=List[TransacionAllOut], status_code=200)
def get_all_transacions(account_number: int, db: Session = Depends(get_db)):
    return get_transactions(db, account_number)


@router.post("/transacao/transferir")
def make_transfer(
    payload: TransferRequest,
    db: Session = Depends(get_db),
    current_user: Account = Depends(get_current_user),
):
    return transfer_amount(db, current_user, payload)
