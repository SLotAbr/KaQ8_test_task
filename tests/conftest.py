import asyncio
from typing import Any, Generator
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, User, Account
from src.database import get_async_session
from src.app import create_app
from src.config import config
from src.security import PasswordHandler


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncSession:
    async_engine = create_async_engine(config.TEST_DATABASE_URL)
    AsyncSessionFactory = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

    async with AsyncSessionFactory() as session:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield session

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def register_test_admin(db_session: AsyncSession) -> None:
    test_admin = User(
        username="ADMIN",
        email=config.ADMIN_EMAIL,
        hashed_password=PasswordHandler.hash_password(config.ADMIN_PASSWORD),
        is_admin=True,
    )
    db_session.add(test_admin)
    await db_session.commit()


@pytest_asyncio.fixture(scope="function")
async def register_test_user(db_session: AsyncSession) -> None:
    test_user = User(
        username="TEST_USER",
        email=config.TEST_USER_EMAIL,
        hashed_password=PasswordHandler.hash_password(config.TEST_USER_PASSWORD),
        is_admin=False,
    )
    db_session.add(test_user)
    await db_session.commit()


@pytest_asyncio.fixture(scope="function")
async def register_test_account(db_session: AsyncSession) -> None:
    test_account = Account(
        amount=1234,
        user_id=2,
        account_id=1,
    )
    db_session.add(test_account)
    await db_session.commit()


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    app = create_app()
    
    yield app



@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, db_session) -> AsyncClient:
    async def _get_session():
        return db_session

    app.dependency_overrides[get_async_session] = _get_session
    
    async with AsyncClient(transport=ASGITransport(app), base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()


