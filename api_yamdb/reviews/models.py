from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    """Model for object category."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', 'slug',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    """Model for object genre."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', 'slug',)

    def __str__(self):
        return self.slug


class Title(models.Model):
    """Model for object's characteristics."""
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        related_name='category',)

    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    description = models.TextField(blank=True)
    name = models.CharField(max_length=256)
    year = models.IntegerField()

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return self.name[:15]


class GenreTitle(models.Model):
    """Model for connection title_id and genre_id."""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} - {self.genre}.'


class Review(models.Model):
    """Model for reviews to object."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведения',
        null=True
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Текст отзыва'
    )
    score = models.IntegerField(
        validators=(
            MinValueValidator(1, 'Рейтинг не может быть меньше единицы.'),
            MaxValueValidator(10, 'Рейтинг не может быть бельше 10.')),
        error_messages={'validators': 'Укажите оценку от 1 до 10'},
        verbose_name='Оценка',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        null=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='unique_review'
            )]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Model for comments to object."""
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.text[:15]
