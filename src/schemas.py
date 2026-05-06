from typing import Optional
from pydantic import BaseModel, Field, EmailStr, UUID4


class ReadAccount(BaseModel):
    account_id: int
    amount: int


class ReadTransaction(BaseModel):
    account_id: int = Field(gt=0)
    amount: int = Field(gt=0)


class RegisterTransaction(ReadTransaction):
    transaction_id: UUID4
    user_id: int = Field(gt=0)
    signature: str


class RegisterUser(BaseModel):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=4, max_length=16)


class ReadUser(BaseModel):
    username: str
    email: str


class ReadUserAccounts(ReadUser):
    accounts: list[ReadAccount]


class UserPartialUpdate(BaseModel):
    username: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str

























