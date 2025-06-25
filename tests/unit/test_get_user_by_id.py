import pytest


@pytest.mark.asyncio
async def test_get_user_by_id(async_client):
    """
    Тестирование получения информации о пользователе по его ID.
    """
    headers = {"api-key": "test1"}
    # Узнаём ID пользователя
    response = await async_client.get("/api/users/me", headers=headers)
    data = response.json()
    user_id = int(data["user"]["id"]) + 1

    # Получаем информацию о пользователе по его ID
    response = await async_client.get(f"/api/users/{user_id}", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True
    assert isinstance(data["user"], dict)
    assert "id" in data["user"] and isinstance(data["user"]["id"], int)
    assert "name" in data["user"] and isinstance(data["user"]["name"], str)
    assert "followers" in data["user"] and isinstance(
        data["user"]["followers"], list
    )
    assert "following" in data["user"] and isinstance(
        data["user"]["following"], list
    )

    for follower in data["user"]["followers"]:
        assert isinstance(follower, dict)
        assert "id" in follower and isinstance(follower["id"], int)
        assert "name" in follower and isinstance(follower["name"], str)

    for following in data["user"]["following"]:
        assert isinstance(following, dict)
        assert "id" in following and isinstance(following["id"], int)
        assert "name" in following and isinstance(following["name"], str)
