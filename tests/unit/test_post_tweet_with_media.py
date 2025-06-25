import pytest
from conftest import images_dir


@pytest.mark.asyncio
async def test_post_tweet_with_media(async_client):
    """
    Тестирование добавления твита с медиафайлами.
    """
    headers = {"api-key": "test1"}

    # Создаем медиафайл для тестирования
    file = {"file": open(images_dir + "/test_image_1.png", "rb")}
    response = await async_client.post(
        "/api/medias", files=file, headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert isinstance(data["media_id"], int)

    # Добавляем твит с медиафайлами
    tweet_data = {
        "tweet_data": "Тестовый твит",
        "tweet_media_ids": [data["media_id"]],
    }

    response = await async_client.post(
        "/api/tweets", json=tweet_data, headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "tweet_id" and "result" in data
    assert isinstance(data["tweet_id"], int)
    assert data["result"] is True
