import pytest


@pytest.mark.asyncio
async def test_like_tweet(async_client):
    """
    Тестирование лайка твита.
    """
    headers = {"api-key": "test1"}

    # Создаём твит для того, чтобы его лайкнуть
    tweet_data = {
        "tweet_data": "Тестовый твит",
        "tweet_media_ids": [],
    }

    response = await async_client.post(
        "/api/tweets", json=tweet_data, headers=headers
    )

    assert response.status_code == 200
    data = response.json()

    # Лайкаем твит по ID
    tweet_id = data["tweet_id"]

    response = await async_client.post(
        f"/api/tweets/{tweet_id}/likes", headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True

    # Лайкаем повторно и ловим ошибку
    response = await async_client.post(
        f"/api/tweets/{tweet_id}/likes", headers=headers
    )

    assert response.status_code == 400

    data = response.json()
    assert data["result"] is False
    assert "error_type" in data and data["error_type"] == "ConflictError"
    assert "error_message" in data

    # Убираем лайк с твита
    response = await async_client.delete(
        f"/api/tweets/{tweet_id}/likes", headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True

    # Убираем лайк повторно и ловим ошибку
    response = await async_client.delete(
        f"/api/tweets/{tweet_id}/likes", headers=headers
    )

    assert response.status_code == 400

    data = response.json()
    assert data["result"] is False
    assert "error_type" in data and data["error_type"] == "NotFoundError"
    assert "error_message" in data
