from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer

User = get_user_model()


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    APIView для редактирования и просмотра профиля любого пользователя.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
