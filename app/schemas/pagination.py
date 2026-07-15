from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(
    GenericModel,
    Generic[T]
):

    page: int

    size: int

    total: int

    total_pages: int

    items: list[T]