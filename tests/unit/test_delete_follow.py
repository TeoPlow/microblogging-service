import pytest


@pytest.mark.asyncio
async def test_delete_follow(async_client):
    """
    Тестирование добавления подписки на пользователя.
    """
    headers = {"api-key": "test1"}
    # Узнаём ID пользователя
    response = await async_client.get("/api/users/me", headers=headers)
    data = response.json()
    user_id = int(data["user"]["id"]) + 1

    # Подписываемся на пользователя перед удалением подписки
    response = await async_client.post(
        f"/api/users/{user_id}/follow", headers=headers
    )

    # Удялаем подписку на пользователя
    response = await async_client.delete(
        f"/api/users/{user_id}/follow", headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True

    # Удаляем подписку ещё раз и ловим ошибку
    response = await async_client.delete(
        f"/api/users/{user_id}/follow", headers=headers
    )
    assert response.status_code == 400

    data = response.json()
    assert data["result"] is False
    assert "error_type" in data and data["error_type"] == "NotFoundError"
    assert "error_message" in data
