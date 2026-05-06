from fastapi import APIRouter
from .users import UsersRouter
from .accounts import AccountsRouter
from .transactions import TransactionsRouter


router = APIRouter()


router.include_router(
    UsersRouter, tags=["users"]
)
router.include_router(
    AccountsRouter, tags=["accounts"]
)
router.include_router(
    TransactionsRouter, prefix="/transactions", tags=["transactions"]
)

