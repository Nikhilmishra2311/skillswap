from minio import Minio
from minio.error import S3Error

from app.core.config import settings


client = Minio(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE,
)


def initialize_bucket():
    try:
        if not client.bucket_exists(settings.MINIO_BUCKET):
            client.make_bucket(settings.MINIO_BUCKET)
            print(f"✅ Bucket '{settings.MINIO_BUCKET}' created.")
        else:
            print(f"✅ Bucket '{settings.MINIO_BUCKET}' already exists.")
    except S3Error as e:
        print(f"❌ MinIO Error: {e}")