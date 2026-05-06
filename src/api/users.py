from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src import schemas
from src.models import User
from src.api.utils import get_user_or_404, check_username, check_user_email
from src.security import PasswordHandler, JWTHandler, get_current_user, get_admin


UsersRouter = APIRouter()


@UsersRouter.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    register_user: schemas.RegisterUser, 
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin),
) -> schemas.ReadUser:
    await check_username(register_user.username, session)
    await check_user_email(register_user.email, session)
    user = User(
        username = register_user.username, 
        email = register_user.email, 
        hashed_password = PasswordHandler.hash_password(
            register_user.password
        )
    )
    session.add(user)
    await session.commit()
    return user


@UsersRouter.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> schemas.Token:
    query = select(User).filter(User.email == form_data.username)
    query = await session.scalars(query)
    user = query.one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email or password"
        )
    if not PasswordHandler.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Incorrect email or password"
        )
    return schemas.Token(
        access_token = JWTHandler.encode(payload={"user_id":user.id}),
        token_type = "bearer"
    )


@UsersRouter.patch("/{id}")
async def patch_user(
    user_patch: schemas.UserPartialUpdate,
    user: User = Depends(get_user_or_404),
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin),
) -> schemas.ReadUser:
    if user_patch_dict.username:
        await check_username(register_user.username, session)
        user.username = user_patch_dict.username
        session.add(user)
        await session.commit()
    return user


@UsersRouter.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user: User = Depends(get_user_or_404),
    session: AsyncSession = Depends(get_async_session),
    admin: User = Depends(get_admin),
):
    await session.delete(user)
    await session.commit()


@UsersRouter.get("/me")
async def get_me(
    user: User = Depends(get_current_user)
) -> schemas.ReadUser:
    return user



















