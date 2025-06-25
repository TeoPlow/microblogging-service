from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi.concurrency import run_in_threadpool
from app.api.v1.models import Tweet, User
from app.config import Config
from app.api.exceptions import SomeError, ApiException, NotFoundError
from app.api.database import minio_client

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def delete_tweet_by_id(
    tweet_id: int,
    session: AsyncSession,
    user: User
):
    """
    Ассинхронная функция для удаления твита по его ID.
    """
    try:
        result = await session.execute(
            select(Tweet)
            .options(selectinload(Tweet.medias))
            .where(Tweet.id == tweet_id)
        )
        log.debug(f"Получил твит с id: {tweet_id}")
        tweet = result.scalar_one_or_none()

        if tweet is None:
            raise NotFoundError(f"Твит с id '{tweet_id}' не найден")

        if tweet.author_id != user.id:
            raise SomeError("У вас нет прав на удаление этого Твита")

        log.debug(f"Удаляю твит с id: {tweet_id} и его медиа файлы")
        for media in tweet.medias:
            try:
                await run_in_threadpool(
                    minio_client.remove_object,
                    bucket_name=Config.MINIO_BUCKET_NAME,
                    object_name=media.filename,
                )
            except Exception as e:
                log.error(
                    f"Ошибка при удалении {media.filename} из MinIO: {e}"
                )
                pass

        await session.delete(tweet)
        await session.commit()

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось удалить твит: {e}"
        log.error(error_message)
        raise SomeError(error_message)
