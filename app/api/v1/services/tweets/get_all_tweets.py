from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from sqlalchemy.orm import selectinload
from typing import List
from app.api.v1.models import Tweet, Like
from app.api.v1.schemas import TweetResponse, SimpleUser, LikeSchema
from app.config import Config
from app.api.exceptions import SomeError, ApiException

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def get_all_tweets(session: AsyncSession) -> List[TweetResponse]:
    """
    Асинхронная функция для получения всех твитов
    без проверки авторизации.
    """
    try:
        result = await session.execute(
            select(Tweet, func.count(Like.tweet_id).label("likes_count"))
            .join(Like, Like.tweet_id == Tweet.id, isouter=True)
            .options(
                selectinload(Tweet.medias),
                selectinload(Tweet.likes).selectinload(Like.user),
                selectinload(Tweet.author),
            )
            .group_by(Tweet.id)
            .order_by(desc("likes_count"))
        )

        rows = result.all()
        tweets = [row[0] for row in rows]

        tweet_list: list[TweetResponse] = []

        for tweet in tweets:
            tweet_list.append(
                TweetResponse(
                    id=tweet.id,
                    content=tweet.content,
                    attachments=[
                        (
                            f"{Config.MINIO_URL}/"
                            f"{Config.MINIO_BUCKET_NAME}/{media.filename}"
                        )
                        for media in tweet.medias
                    ],
                    author=SimpleUser(
                        id=tweet.author.id,
                        name=tweet.author.name,
                    ),
                    likes=[
                        LikeSchema(user_id=like.user.id, name=like.user.name)
                        for like in tweet.likes
                    ],
                )
            )

        return tweet_list

    except ApiException as e:
        raise e
    except Exception as e:
        error_message = f"Не удалось получить твиты: {e}"
        log.error(error_message)
        raise SomeError(error_message)
