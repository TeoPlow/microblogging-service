import pytest


@pytest.mark.asyncio
async def test_post_follow(async_client):
    """
    Тестирование добавления подписки на пользователя.
    """
    headers = {"api-key": "test1"}
    # Узнаём ID пользователя
    response = await async_client.get("/api/users/me", headers=headers)
    data = response.json()
    user_id = int(data["user"]["id"]) + 1

    # Удаляем подписку на пользователя заранее
    response = await async_client.delete(
        f"/api/users/{user_id}/follow", headers=headers
    )

    # Подписываемся на пользователя
    response = await async_client.post(
        f"/api/users/{user_id}/follow", headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True

    # Подписываемся ещё раз и ловим ошибку
    response = await async_client.post(
        f"/api/users/{user_id}/follow", headers=headers
    )

    assert response.status_code == 400

    data = response.json()
    assert data["result"] is False
    assert "error_type" in data and data["error_type"] == "ConflictError"
    assert "error_message" in data
