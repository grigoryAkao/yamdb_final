from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    """Serializing model 'Comment'."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    """Serializing model 'Genre'."""
    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class CategorySerializer(serializers.ModelSerializer):
    """Serializing model 'Genre'."""
    class Meta:
        model = Category
        fields = ('name', 'slug',)

    def create(self, validated_data):
        return Category.objects.create(**validated_data)


class TitleSerializer(serializers.ModelSerializer):
    """Serializing model 'Title'."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleDetailSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializing model 'Review'."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        required=False,
    )
    text = serializers.CharField(allow_blank=True, required=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError('Можно оставлять не более одного отзыва!')
        return data
