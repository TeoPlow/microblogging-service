import pytest


@pytest.mark.asyncio
async def test_get_tweets(async_client):
    """
    Тестирование получения твитов.
    """
    headers = {"api-key": "test1"}

    response = await async_client.get("/api/tweets", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["result"] is True
    assert isinstance(data["tweets"], list)

    for tweet in data["tweets"]:
        assert isinstance(tweet["id"], int)
        assert isinstance(tweet["content"], str)
        assert isinstance(tweet["attachments"], list)
        assert all(isinstance(link, str) for link in tweet["attachments"])
        assert isinstance(tweet["author"], dict)
        assert "id" in tweet["author"] and isinstance(
            tweet["author"]["id"], int
        )
        assert "name" in tweet["author"] and isinstance(
            tweet["author"]["name"], str
        )
        assert isinstance(tweet["likes"], list)
        for like in tweet["likes"]:
            assert isinstance(like, dict)
            assert "user_id" in like and isinstance(like["user_id"], int)
            assert "name" in like and isinstance(like["name"], str)
