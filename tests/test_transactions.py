import pytest
from httpx import AsyncClient

from src.security import SignatureHandler
from tests.utils import (
    _client_authorization,
)


@pytest.mark.asyncio
async def test_transactions(
    register_test_admin,
    register_test_user,
    client: AsyncClient,
) -> None:
    transaction_data = {
        "transaction_id": "4504dbf9-ecc4-4228-8c15-c7ca64be1591",
        "account_id": 2,
        "user_id": 2,
        "amount": 100,
    }
    transaction_data.update(
        {"signature": SignatureHandler.hash_signature(transaction_data)}
    )
    response = await client.post("/transactions/", json=transaction_data)
    
    await _client_authorization(client, as_admin=True)
    
    response = await client.get("/list_users")
    assert response.json()[-1]["accounts"][0]["account_id"] == 2
    assert response.json()[-1]["accounts"][0]["amount"] == 100
    
    response = await client.get("/my_transactions")
    assert response.status_code == 403
    
    await _client_authorization(client, as_admin=False)
    
    response = await client.get("/my_transactions")
    assert response.json()[0]["account_id"] == 2
    assert response.json()[0]["amount"] == 100
    
    response = await client.get("/my_accounts")
    assert response.json()[0]["account_id"] == 2
    assert response.json()[0]["amount"] == 100



















