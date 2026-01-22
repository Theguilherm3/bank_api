from pydantic import BaseModel


class LoginIn(BaseModel):
    account: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
