from fastapi import APIRouter, UploadFile, File, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.api.v1.services.users import get_user_by_api_key
from app.api.database import get_db, get_redis_client
from app.api.v1.services.medias import save_media
from app.api.v1.schemas import MediaResponse, error_responses
from app.api.utils.logger import get_logger

log = get_logger("MediaRouterLogger")

router = APIRouter()


@router.post("", response_model=MediaResponse, responses=error_responses)
async def post_media(
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis_client),
    file: UploadFile = File(...),
    api_key: str = Header(None, alias="api-key"),
) -> MediaResponse:
    """
    Эндпоинт для загрузки медиа-файлов.
    Принимает файл и сохраняет его в базе данных.
    Возвращает cловарь с результатом операции и ID сохраненного медиа.
    """
    log.debug(f"Обработка запроса на добавление медиа - {file.filename}")

    await get_user_by_api_key(session, redis_client, api_key)

    media = await save_media(file, session)

    return MediaResponse(media_id=int(media.id))
