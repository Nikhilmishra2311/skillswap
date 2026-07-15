import json

from app.core.cache import redis_client
from app.core.config import settings


def get_cache(key: str):

    data = redis_client.get(key)

    if data:

        return json.loads(data)

    return None


def set_cache(

    key: str,

    value,

    expire: int = settings.CACHE_EXPIRE

):

    redis_client.setex(

        key,

        expire,

        json.dumps(

            value,

            default=str

        )

    )


def delete_cache(

    key: str

):

    redis_client.delete(key)


def delete_pattern(

    pattern: str

):

    keys = redis_client.keys(pattern)

    if keys:

        redis_client.delete(*keys)