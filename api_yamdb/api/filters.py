import django_filters
from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """Фильтр произведений по имени, жанру или категрии."""

    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr='contains'
    )
    genre = django_filters.CharFilter(
        field_name="genre__slug",
        method='filter_genre'
    )
    category = django_filters.CharFilter(
        field_name="category__slug",
        lookup_expr='exact'
    )

    class Meta:
        model = Title
        fields = ('name', 'genre', 'category', 'year')

    def filter_genre(self, queryset, slug, genre):
        return queryset.filter(genre__slug__in=genre.split(','))
