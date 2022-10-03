from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly,
                          IsAuthorIsModeratorIsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleDetailSerializer, TitleSerializer)


class ListOrCreateDestroyViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Create custom viewset."""
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset for model 'Title'."""
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    serializer_class = TitleSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('genre',)
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return TitleDetailSerializer
        return TitleSerializer


class GenreViewSet(ListOrCreateDestroyViewSet):
    """Viewset for model 'Genre'."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(ListOrCreateDestroyViewSet):
    """Viewset for model 'Category'."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Viewset for model 'Review'."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorIsModeratorIsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for model 'Comment'."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorIsModeratorIsAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
