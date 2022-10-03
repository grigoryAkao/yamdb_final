from uuid import uuid4

from api.permissions import IsAdmin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import decorators, filters, status, views, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import (
    CreateUserTokenSerializer, SignupUserSerializer,
    UserSerializer, UserCantChageRoleSerializer)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет ресурса users.
    Нужен для работы админа с учетными записями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    pagination_class = PageNumberPagination
    permission_classes = (IsAdmin, )

    filter_backends = (filters.SearchFilter, )
    lookup_field = 'username'

    def get_instance(self):
        return self.request.user

    @decorators.action(
        detail=False, methods=['get', 'patch'],
        permission_classes=(IsAuthenticated, )
    )
    def me(self, request, *args, **kwargs):
        """Метод создает ресурс me."""

        self.get_object = self.get_instance

        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PATCH':
            data = request.data.copy()
            serialized = UserCantChageRoleSerializer(
                request.user,
                data=data,
                partial=True
            )
            if serialized.is_valid(raise_exception=True):
                serialized.save()
                return Response(serialized.data)
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class CreateUserAPIView(views.APIView):
    """Вьюсет для ресурса signup."""

    permission_classes = ()

    def post(self, request):
        serializer = SignupUserSerializer(data=request.data)
        confirmation_code = str(uuid4())
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['confirmation_code'] = confirmation_code
            user = serializer.save()
            send_mail(
                'Ваш код для подтверждения: ',
                confirmation_code,
                ['test@test.com'],
                (user.email, ),
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return None


class CreateTokenAPIView(views.APIView):
    """Вьюсет для ресурса tokens.
    Принимает код из e-mail и возвращает токен.
    """

    permission_classes = ()

    def post(self, request):
        serializer = CreateUserTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            current_user = get_object_or_404(
                User,
                username=username
            )
            if serializer.validated_data['username'].lower() == 'me':
                return Response(
                    serializer.data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            elif confirmation_code == current_user.confirmation_code:
                token = str(AccessToken.for_user(current_user))
                return Response(
                    {'token': token, },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return None
