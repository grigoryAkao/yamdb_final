from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import AccessToken

from .models import User

CLOSED_USERNAMES = ['me', ]


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для эндпоинта users.
    Простая обработка модели."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserCantChageRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        read_only_fields = ("role",)


class SignupUserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User для регистрации."""
    username = serializers.CharField()
    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким email уже зарегистрирован'
        )]
    )

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if (value.lower() in CLOSED_USERNAMES
                or User.objects.filter(username=value).exists()):
            raise serializers.ValidationError(
                'Выбранное имя недопустимо, выберите другое.'
            )
        return value


class CreateUserTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер модели User для регистрации."""
    username = serializers.CharField()
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code',
        )

    def validate(self, attrs):
        user = get_object_or_404(
            User,
            username=attrs.get('username')
        )
        if attrs.get('confirmation_code') != user.confirmation_code:
            raise serializers.ValidationError(
                'Указан неверный код.'
            )
        token = AccessToken.for_user(user)
        return {'access_token': str(token.access_token)}
