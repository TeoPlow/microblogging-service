import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database import minio_client
from fastapi import UploadFile
from app.api.v1.models import Media
from app.config import Config
from app.api.exceptions import SomeError

from app.api.utils.logger import get_logger

log = get_logger("MediaRouterLogger")


async def save_media(
        file: UploadFile,
        session: AsyncSession,
) -> Media:
    """
    Ассинхронная функция сохранения файлов в S3 хранилище MinIO
    и добавление записей о файлах в БД.
    """
    try:
        log.debug(f"Начинаю сохранять файл - file: {file.filename}")
        if not file.filename:
            raise SomeError("Файл не содержит имени")
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"

        log.debug(f"Переименовал файл - {file.filename} в {filename}")

        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)

        log.debug(f"""
            Сохраняю файл в MinIO -
            bucket: {Config.MINIO_BUCKET_NAME}, object_name: {filename}
        """)
        minio_client.put_object(
            bucket_name=Config.MINIO_BUCKET_NAME,
            object_name=filename,
            data=file.file,
            length=file_size,
            content_type=file.content_type or "application/octet-stream",
        )

        log.debug("Записываю информацию о файле в базу данных")
        media = Media(filename=filename)
        session.add(media)
        await session.commit()
        await session.refresh(media)

        return media

    except Exception as e:
        await session.rollback()
        error_message = f"Ошибка при сохранении файла: {e}"
        log.error(error_message)
        raise SomeError(error_message)
