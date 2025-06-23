from app.api.v1.schemas import TweetSendRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Media, Tweet
from sqlalchemy import update
from app.api.v1.services.users import get_user_by_api_key
from app.api.exceptions import SomeError, ApiException

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def send_tweet(
    data: TweetSendRequest, api_key: str, session: AsyncSession
):
    try:
        user = await get_user_by_api_key(session, api_key)

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

        return tweet.id

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось создать твит: {e}"
        log.error(error_message)
        raise SomeError(error_message)
