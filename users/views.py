from django.contrib.auth import get_user_model
from rest_framework.generics import (CreateAPIView, ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, UserUpdateSerializer

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    """
    Создание пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListView(ListCreateAPIView):
    """
    Просмотр пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class UserDetailView(RetrieveUpdateDestroyAPIView):
    """
    Просмотр профиля пользователя.
    """

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
