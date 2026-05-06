import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import (
    _client_authorization,
)


@pytest.mark.asyncio
async def test_accounts(
    register_test_admin,
    register_test_user,
    register_test_account,
    client: AsyncClient, 
    db_session: AsyncSession
) -> None:
    await _client_authorization(client, as_admin=True)
    
    response = await client.get("/list_users")
    assert response.json()[0]["accounts"][0]["account_id"] is not None
    assert response.json()[0]["accounts"][0]["amount"] is not None





































