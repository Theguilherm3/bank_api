from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.security import create_access_token, verify_password
from models.accounts import Account
from schemas.login import LoginIn


def login(db: Session, login: LoginIn):
    account = db.query(Account).filter(Account.account_number == login.account).first()

    if not account:
        raise HTTPException(status_code=401, detail="Conta ou senha incorretos")

    if not verify_password(login.password, account.password):
        raise HTTPException(status_code=401, detail="Conta ou senha incorretos")

    access_token = create_access_token({"sub": str(login.account)})

    return {"access_token": access_token, "token_type": "bearer"}
