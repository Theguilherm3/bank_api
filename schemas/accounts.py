from pydantic import BaseModel


class AccountCreate(BaseModel):
    username: str = "Seu Nome"
    balance: float = 6025.54


class AccountOut(BaseModel):
    id: int
    username: str
    account_number: int
    balance: float
