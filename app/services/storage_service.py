import uuid
from io import BytesIO

from fastapi import UploadFile, HTTPException
from minio.error import S3Error

from app.core.minio import client
from app.core.config import settings


ALLOWED_IMAGE_TYPES = {

    "image/jpeg",

    "image/png",

    "image/webp"

}

MAX_IMAGE_SIZE = 5 * 1024 * 1024


def upload_image(

    file: UploadFile,

    folder: str

) -> str:

    # ============================
    # Validate Content Type
    # ============================

    if file.content_type not in ALLOWED_IMAGE_TYPES:

        raise HTTPException(

            status_code=400,

            detail="Only JPG, PNG and WEBP are allowed."

        )

    # ============================
    # Read File
    # ============================

    data = file.file.read()

    if len(data) > MAX_IMAGE_SIZE:

        raise HTTPException(

            status_code=400,

            detail="Image size exceeds 5 MB."

        )

    # ============================
    # Unique File Name
    # ============================

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"

    object_name = f"{folder}/{filename}"

    # ============================
    # Upload
    # ============================

    try:

        client.put_object(

            bucket_name=settings.MINIO_BUCKET,

            object_name=object_name,

            data=BytesIO(data),

            length=len(data),

            content_type=file.content_type

        )

    except S3Error as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )

    return object_name


def get_file_url(

    object_name: str

):

    return (

        f"http://localhost:9000/"

        f"{settings.MINIO_BUCKET}/"

        f"{object_name}"

    )


def delete_file(

    object_name: str

):

    try:

        client.remove_object(

            settings.MINIO_BUCKET,

            object_name

        )

    except Exception:

        pass