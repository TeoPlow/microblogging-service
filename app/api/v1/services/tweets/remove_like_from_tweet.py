from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Tweet, Like, User
from app.api.exceptions import SomeError, ApiException, NotFoundError

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def remove_like_from_tweet(
    tweet_id: int, session: AsyncSession, user: User
):
    """
    Ассинхронная функция для удаления лайка из твита.
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
        like = like_result.scalar_one_or_none()
        if like is None:
            raise NotFoundError(
                f"Лайк от пользователя {user.id} не найден"
            )

        await session.execute(
            delete(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == user.id
            )
        )
        await session.commit()

        log.debug(
            f"Пользователь {user.id} удалил лайк с твита {tweet_id}"
        )

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось удалить лайк: {e}"
        log.error(error_message)
        raise SomeError(error_message)
