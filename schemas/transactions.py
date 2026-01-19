from datetime import date

from pydantic import BaseModel

from models.transactions import EnumPaymentTypes


class TransactionCreate(BaseModel):
    id: str
    user_id: str
    transaction_type: EnumPaymentTypes
    amount: float
    date: date


class TransactionOut(BaseModel):
    account_id: str
    balance: int


class AccountCreate(BaseModel):
    username: str


class AccountOut(BaseModel):
    account_id: int
    balance: int
