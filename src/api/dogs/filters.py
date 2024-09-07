from django_filters.rest_framework import CharFilter, FilterSet

from src.core.models import Bread


class BreadFilter(FilterSet):
    name = CharFilter(method="filter_name")

    class Meta:
        model = Bread
        fields = (
            "name",
            "description",
        )

    def filter_name(self, queryset, name, value):
        names = value.split(",")
        return queryset.filter(name__in=names)
