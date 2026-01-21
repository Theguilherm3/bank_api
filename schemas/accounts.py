from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    username: str = "Seu Nome"
    balance: float = Field(gt=0, default=5412)


class AccountOut(BaseModel):
    id: int
    username: str
    account_number: int
    balance: float
