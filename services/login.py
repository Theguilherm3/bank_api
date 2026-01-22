from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.security import create_access_token, verify_password
from models.accounts import Account


def login(db: Session, login: OAuth2PasswordRequestForm):
    try:
        account_number_input = int(login.username)
    except ValueError:
        raise HTTPException(status_code=401, detail="Numero de conta inválido")

    account = (
        db.query(Account).filter(Account.account_number == account_number_input).first()
    )

    if not account or not verify_password(login.password, account.password):
        raise HTTPException(status_code=401, detail="Conta ou senha incorretos")

    access_token = create_access_token({"sub": str(account_number_input)})

    return {"access_token": access_token, "token_type": "bearer"}
