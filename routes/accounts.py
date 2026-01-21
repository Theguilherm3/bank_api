from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from schemas.accounts import AccountCreate, AccountOut
from services.accounts import create_account, get_balance

router = APIRouter()


@router.post("/conta/criar", response_model=AccountOut, status_code=200)
def create_new_account(payload: AccountCreate, db=Depends(get_db)):
    return create_account(db, payload)


@router.get("/conta", response_model=AccountOut, status_code=200)
def get_account_balance(account_number: int, db: Session = Depends(get_db)):
    return get_balance(db, account_number)
