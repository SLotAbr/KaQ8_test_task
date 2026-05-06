from fastapi import FastAPI
import contextlib
from src.database import (
    register_admin, 
    register_test_user_and_account
)

from src.api import router


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_all_tables()
    await register_admin()
    await register_test_user_and_account()
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(
        lifespan = lifespan, 
    )
    app_.include_router(
        router,
    )
    return app_


app = create_app()

