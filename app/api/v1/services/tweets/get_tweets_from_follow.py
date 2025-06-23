from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from app.api.v1.models import Tweet, Like, Follower
from app.config import Config
from app.api.v1.services.users import get_user_by_api_key
from app.api.exceptions import SomeError, ApiException

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def get_tweets_from_follow(session: AsyncSession, api_key: str):
    """
    Асинхронная функция для получения твитов от пользователей,
    на которых подписан текущий пользователь.
    Также список твитов возвращается по убыванию популярности.
    """
    try:
        current_user = await get_user_by_api_key(session, api_key)

        log.debug(
            f"Получаю ID интересующих пользователей: {current_user.id}"
        )
        result = await session.execute(
            select(Follower.user_id).where(
                Follower.follower_id == current_user.id
            )
        )
        following_user_ids = [row[0] for row in result.all()]

        if not following_user_ids:
            return []

        log.debug(
            f"Получаю твиты интересующих пользователей: {following_user_ids}"
        )
        result = await session.execute(
            select(Tweet)
            .join(Like, Like.tweet_id == Tweet.id, isouter=True)
            .where(Tweet.author_id.in_(following_user_ids))
            .options(
                selectinload(Tweet.medias),
                selectinload(Tweet.likes).selectinload(Like.user),
                selectinload(Tweet.author),
            )
            .group_by(Tweet.id)
            .order_by(desc(func.count(Like.id)))
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
