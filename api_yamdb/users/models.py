from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Создание модели User."""

    admin = 'admin'
    moderator = 'moderator'
    user = 'user'

    PERMISSION_CHOICES = [
        (admin, 'admin'),
        (moderator, 'moderator'),
        (user, 'user'),
    ]

    username = models.CharField(
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    role = models.CharField(
        'Роль пользователя',
        choices=PERMISSION_CHOICES,
        default='user',
        max_length=100,
    )
    bio = models.TextField(
        'Биография пользователя',
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=150,
        blank=True
    )

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.admin

    @property
    def is_moderator(self):
        return self.role == self.moderator

    @property
    def is_user(self):
        return self.role == self.user

    class Meta:
        ordering = ['username']
