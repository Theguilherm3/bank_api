from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.transactions import TransactionOut
from services.transactions import get_transactions

router = APIRouter()


@router.get("/transactions", response_model=list[TransactionOut], status_code=200)
def get_list_of_transactions(account_id: int, db: Session = Depends(get_db)):
    return get_transactions(db, account_id)
