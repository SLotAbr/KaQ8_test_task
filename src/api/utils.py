from typing import Union
from pydantic import ValidationError
from fastapi import status, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src import schemas
from src.models import User, Transaction, Account
from src.security import SignatureHandler


async def get_user_or_404(
    id: int, session: AsyncSession = Depends(get_async_session),
) -> User:
    query = select(User).where(User.id == id)
    query = await session.scalars(query)
    user = query.one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User with given uuid is not found"
        )
    return user


async def check_username(
    usernme: str, session: AsyncSession = Depends(get_async_session),
) -> None:
    query = select(User).filter(User.username == username)
    query = await session.scalars(query)
    user = query.one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this username already exists"
        )


async def check_user_email(
    email: str, session: AsyncSession = Depends(get_async_session),
) -> None:
    query = select(User).filter(User.email == email)
    query = await session.scalars(query)
    user = query.one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with this email already exists"
        )


async def validate_transaction_data(
    data: dict,
    session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        register_transaction = schemas.RegisterTransaction(**data)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Data validation failed"
        )
    transaction_dict = register_transaction.model_dump()
    SignatureHandler.verify_signature(transaction_dict)
    
    query = select(Transaction).filter(
        Transaction.transaction_id == transaction_dict["transaction_id"]
    )
    query = await session.scalars(query)
    transaction = query.one_or_none()
    if transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Transaction with this id already exists"
        )
    
    return transaction_dict


async def get_account(
    user_id: int, account_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> Union[Account | None]:
    query = select(Account).filter(
        Account.user_id == user_id,
        Account.account_id == account_id
    )
    query = await session.scalars(query)
    account = query.one_or_none()
    return account





























