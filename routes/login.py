from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.session import get_db
from models.accounts import Account
from schemas.login import Token
from services.login import login

router = APIRouter()


@router.post("/login", response_model=Token)
def login_account(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return login(db, form_data)


@router.get("/me")
def read_users_me(current_user: Account = Depends(get_current_user)):
    return current_user
