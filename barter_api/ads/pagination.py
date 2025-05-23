from rest_framework.pagination import PageNumberPagination

from .constants import (
    PAGE_SIZE, PAGE_SIZE_MAX,
    PAGE_SIZE_QUERY_PARAM, PAGE_QUERY_PARAM
)


class AdsPagination(PageNumberPagination):
    """Пагинация для ads."""

    page_size = PAGE_SIZE
    page_size_query_param = PAGE_SIZE_QUERY_PARAM
    max_page_size = PAGE_SIZE_MAX
    page_query_param = PAGE_QUERY_PARAM
