import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    search = django_filters.CharFilter(method='filter_search')
    is_ready_to_cook = django_filters.BooleanFilter(field_name='is_ready_to_cook')
    is_popular = django_filters.BooleanFilter(field_name='is_popular')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'search', 'is_ready_to_cook', 'is_popular']

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(
            django_filters.db.models.Q(name__icontains=value) | 
            django_filters.db.models.Q(description__icontains=value)
        )
