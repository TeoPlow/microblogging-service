from minio import Minio
from app.config import Config


minio_client = Minio(
    Config.MINIO_ENDPOINT,
    access_key=Config.MINIO_ACCESS_KEY,
    secret_key=Config.MINIO_SECRET_KEY,
    secure=False,
)

found = minio_client.bucket_exists(Config.MINIO_BUCKET_NAME)
if not found:
    minio_client.make_bucket(Config.MINIO_BUCKET_NAME)
