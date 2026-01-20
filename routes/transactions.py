from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.transactions import TransacionAllOut, TransactionCreate
from services.transactions import create_transacion, get_transactions

router = APIRouter()


@router.post("/transacao", response_model=TransactionCreate, status_code=200)
def create_new_transaction(payload: TransactionCreate, db=Depends(get_db)):
    return create_transacion(db, payload)


@router.get("/transacao/all", response_model=List[TransacionAllOut], status_code=200)
def get_all_transacions(account_number: int, db: Session = Depends(get_db)):
    return get_transactions(db, account_number)
