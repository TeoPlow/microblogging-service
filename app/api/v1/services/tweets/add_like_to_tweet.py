from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Tweet, Like, User
from app.api.exceptions import (
    ApiException,
    NotFoundError,
    ConflictError,
    SomeError
)

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def add_like_to_tweet(
    tweet_id: int,
    session: AsyncSession,
    user: User
):
    """
    Ассинхронная функция для добавления лайка к твиту.
    """
    try:

        tweet_result = await session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        tweet = tweet_result.scalar_one_or_none()
        if tweet is None:
            raise NotFoundError(f"Твит с id {tweet_id} не найден")

        like_result = await session.execute(
            select(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == user.id
            )
        )
        existing_like = like_result.scalar_one_or_none()
        if existing_like:
            raise ConflictError("Пользователь уже лайкнул этот твит")

        like = Like(tweet_id=tweet_id, user_id=user.id)
        session.add(like)
        await session.commit()

        log.debug(f"Пользователь {user.id} лайкнул твит {tweet_id}")

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось лайкнуть твит: {e}"
        log.error(error_message)
        raise SomeError(error_message)
