import django_filters

from .models import Todo


class TodoFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    language = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Todo
        fields = {'title': ['icontains'],
                  'description': ['icontains'],
                  'language': ['icontains'],
        }
