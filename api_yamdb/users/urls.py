from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CreateTokenAPIView, CreateUserAPIView, UserViewSet

app_name = 'users'

router = DefaultRouter()
router.register(
    'users',
    UserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', CreateUserAPIView.as_view()),
    path('token/', CreateTokenAPIView.as_view()),
]
