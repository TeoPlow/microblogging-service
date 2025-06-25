from app.api.v1.schemas import TweetSendRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Media, Tweet, User
from sqlalchemy import update
from app.api.exceptions import SomeError, ApiException

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def send_tweet(
    data: TweetSendRequest, user: User, session: AsyncSession
) -> int:
    """
    Ассинхронная функция для отправки твита.
    """
    try:
        tweet = Tweet(content=data.tweet_data, author_id=user.id)
        session.add(tweet)
        await session.flush()

        if data.tweet_media_ids:
            await session.execute(
                update(Media)
                .where(Media.id.in_(data.tweet_media_ids))
                .values(tweet_id=tweet.id)
            )

        await session.commit()

        return int(tweet.id)

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось создать твит: {e}"
        log.error(error_message)
        raise SomeError(error_message)
