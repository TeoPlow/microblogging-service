from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Tweet, Like
from app.api.v1.services.users import get_user_by_api_key
from app.api.exceptions import SomeError, ApiException, NotFoundError

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def add_like_to_tweet(
    tweet_id: int, session: AsyncSession, api_key: str
):
    """
    Ассинхронная функция для добавления лайка к твиту.
    """
    try:
        current_user = await get_user_by_api_key(session, api_key)

        tweet_result = await session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        tweet = tweet_result.scalar_one_or_none()
        if tweet is None:
            raise NotFoundError(f"Твит с id {tweet_id} не найден")

        like_result = await session.execute(
            select(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == current_user.id
            )
        )
        existing_like = like_result.scalar_one_or_none()
        if existing_like:
            raise SomeError("Пользователь уже лайкнул твит")

        like = Like(tweet_id=tweet_id, user_id=current_user.id)
        session.add(like)
        await session.commit()

        log.debug(f"Пользователь {current_user.id} лайкнул твит {tweet_id}")

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось лайкнуть твит: {e}"
        log.error(error_message)
        raise SomeError(error_message)
