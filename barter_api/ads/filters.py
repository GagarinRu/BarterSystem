from django_filters import CharFilter, DateFilter, FilterSet
from django.db import models

from .models import Ad


class AdFilter(FilterSet):
    """Фильтр для объявлений."""

    search = CharFilter(
        method='filter_search',
        label="Поиск по заголовку и описанию"
    )
    min_date = DateFilter(
        field_name='created_at',
        lookup_expr='gte',
        label="Дата от"
    )
    max_date = DateFilter(
        field_name='created_at',
        lookup_expr='lte',
        label="Дата до"
    )

    class Meta:
        model = Ad
        fields = {
            'category': ['exact'],
            'condition': ['exact'],
            'user': ['exact'],
        }

    def filter_search(self, queryset, name, value):
        """Фильтрация по поисковому запросу в заголовке и описании."""
        return queryset.filter(
            models.Q(title__icontains=value) |
            models.Q(description__icontains=value)
        )
