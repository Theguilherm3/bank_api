from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.session import get_db
from models.accounts import Account
from schemas.login import LoginIn, Token
from services.login import login

router = APIRouter()


@router.post("/login", response_model=Token)
def login_account(payload: LoginIn, db: Session = Depends(get_db)):
    return login(db, payload)


@router.get("/me")
def read_users_me(current_user: Account = Depends(get_current_user)):
    return current_user
