from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.api.v1.models import Tweet, Like
from app.config import Config
from app.api.exceptions import SomeError, ApiException

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def get_all_tweets(session: AsyncSession):
    """
    Асинхронная функция для получения всех твитов
    без проверки авторизации.
    """
    try:
        result = await session.execute(
            select(Tweet).options(
                selectinload(Tweet.medias),
                selectinload(Tweet.likes).selectinload(Like.user),
                selectinload(Tweet.author),
            )
        )
        tweets = result.scalars().unique().all()

        tweet_list = []

        for tweet in tweets:
            tweet_list.append(
                {
                    "id": tweet.id,
                    "content": tweet.content,
                    "attachments": [
                        (
                            f"http://{Config.MINIO_ENDPOINT}/"
                            f"{Config.MINIO_BUCKET_NAME}/{media.filename}"
                        )
                        for media in tweet.medias
                    ],
                    "author": {
                        "id": tweet.author.id,
                        "name": tweet.author.name,
                    },
                    "likes": [
                        {"user_id": like.user.id, "name": like.user.name}
                        for like in tweet.likes
                    ],
                }
            )

        return tweet_list

    except ApiException as e:
        raise e
    except Exception as e:
        error_message = f"Не удалось получить твиты: {e}"
        log.error(error_message)
        raise SomeError(error_message)
