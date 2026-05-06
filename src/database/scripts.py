from .sessions import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import User, Account
from src.security import PasswordHandler
from src.config import config


async def register_admin(
    # session: AsyncSession = Depends(get_async_session),
) -> None:
    async with async_session_maker() as session:
        query = select(User).where(User.email == config.ADMIN_EMAIL)
        query = await session.scalars(query)
        admin = query.one_or_none()
        if not admin:
            admin = User(
                username="ADMIN",
                email=config.ADMIN_EMAIL,
                hashed_password=PasswordHandler.hash_password(
                    config.ADMIN_PASSWORD
                ),
                is_admin=True,
            )
            session.add(admin)
            await session.commit()


async def register_test_user_and_account(
    # session: AsyncSession = Depends(get_async_session),
) -> None:
    async with async_session_maker() as session:
        query = select(User).where(User.email == config.TEST_USER_EMAIL)
        query = await session.scalars(query)
        user = query.one_or_none()
        if not user:
            user = User(
                username="TEST_USER",
                email=config.TEST_USER_EMAIL,
                hashed_password=PasswordHandler.hash_password(
                    config.TEST_USER_PASSWORD
                ),
                is_admin=False,
            )
            session.add(user)
            await session.commit()
        
        query = select(Account).filter(
            Account.user_id == user.id,
            Account.account_id == 0
        )
        query = await session.scalars(query)
        account = query.one_or_none()
        if not account:
            account = Account(
                amount = 0,
                user = user,
                account_id = 0,
            )
            session.add(account)
            await session.commit()

