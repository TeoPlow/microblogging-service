import pytest


@pytest.mark.asyncio
async def test_invalid_api_key(async_client):
    """
    Тестирование отсутствия API ключа.
    """
    headers = {}
    # Узнаём ID пользователя
    response = await async_client.get("/api/users/me", headers=headers)
    data = response.json()

    assert data["result"] is False
    assert "error_type" in data and data["error_type"] == "InvalidApiKey"
    assert "error_message" in data
