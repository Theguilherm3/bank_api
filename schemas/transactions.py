from datetime import date

from pydantic import BaseModel, Field

from models.transactions import EnumMovmentType, EnumPaymentTypes


class TransactionCreate(BaseModel):
    movment_type: EnumMovmentType = EnumMovmentType.SAIDA
    transaction_type: EnumPaymentTypes
    account_id: int
    amount: float = Field(gt=0, examples=[129.97])


class TransactionOut(BaseModel):
    account_number: int
    balance: float


class TransacionAllOut(BaseModel):
    id: int
    movment_type: EnumMovmentType
    transaction_type: EnumPaymentTypes
    amount: float
    date: date
