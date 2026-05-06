from httpx import AsyncClient
from src.config import config


async def _client_authorization(client: AsyncClient, as_admin=False):
    if as_admin:
        credentials = {
            "username": config.ADMIN_EMAIL,
            # "email": config.ADMIN_EMAIL,
            "password": config.ADMIN_PASSWORD,
        }
    else:
        credentials = {
            "username": config.TEST_USER_EMAIL,
            "password": config.TEST_USER_PASSWORD,
        }
    response = await client.post("/token", data=credentials)
    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})
    return None

