import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__category_name', lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['category']