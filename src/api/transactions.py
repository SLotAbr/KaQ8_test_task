from fastapi import APIRouter, status, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src import schemas
from src.models import Account, Transaction
from src.api.utils import validate_transaction_data, get_user_or_404, get_account


TransactionsRouter = APIRouter()


@TransactionsRouter.post("/", status_code=status.HTTP_201_CREATED)
async def receive_transaction(
    request: Request, 
    session: AsyncSession = Depends(get_async_session),
) -> schemas.RegisterTransaction:
    data = await request.json()
    transaction_dict = await validate_transaction_data(data, session)
    user = await get_user_or_404(transaction_dict["user_id"], session)
    if user.is_admin == True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="This account can't receive transactions"
        )
    
    account = await get_account(
        transaction_dict["user_id"], transaction_dict["account_id"], 
        session
    )
    if not account:
        account = Account(
            amount = 0,
            user = user,
            account_id = transaction_dict["account_id"],
        )
    account.amount += transaction_dict["amount"]
    session.add(account)
    await session.commit()
    
    transaction = Transaction(**transaction_dict)
    session.add(transaction)
    await session.commit()
    return transaction





































