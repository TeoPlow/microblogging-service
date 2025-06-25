import pytest


@pytest.mark.asyncio
async def test_main_page(async_client):
    """
    Тестирование работоспособности сервиса.
    """
    response = await async_client.get("/")
    assert response.status_code == 200
