from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src import schemas
from src.models import User, Account, Transaction
from src.security import get_user, get_admin


AccountsRouter = APIRouter()


@AccountsRouter.get("/my_accounts")
async def get_my_accounts(
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[schemas.ReadAccount]:
    query = select(Account).where(Account.user_id == user.id)
    results = await session.execute(query)
    return results.scalars().all()


@AccountsRouter.get("/my_transactions")
async def get_my_transactions(
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_async_session),
) -> list[schemas.ReadTransaction]:
    query = select(Transaction).where(Transaction.user_id == user.id)
    results = await session.execute(query)
    return results.scalars().all()


@AccountsRouter.get("/list_users")
async def list_users(
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin)
) -> list[schemas.ReadUserAccounts]:
    query = select(User).where(User.is_admin == False)
    results = await session.execute(query)
    return results.scalars().all()



































