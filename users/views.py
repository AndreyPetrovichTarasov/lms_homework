from django.contrib.auth import get_user_model

from rest_framework import status

from rest_framework.generics import (
    CreateAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from lms.models import Course
from .models import Payment
from .services.stripe_service import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_checkout_session,
)

from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer, UserUpdateSerializer, PaymentSerializer

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


class PaymentViewSet(ModelViewSet):
    """
    ViewSet для работы с платежами.
    """

    queryset = Payment.objects.select_related("user", "course", "lesson")
    serializer_class = PaymentSerializer

    @action(detail=False, methods=["post"], url_path="stripe/create")
    def create_stripe_payment(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course = get_object_or_404(Course, id=course_id)

        # Вместо price из модели Course, используем фиксированную цену или передаем ее в запросе
        price = request.data.get("price")  # Получаем цену из запроса (в копейках)
        if not price:
            return Response({"error": "Цена курса не передана."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем продукт и цену в Stripe
        stripe_product_id = create_stripe_product(course.name)
        stripe_price_id = create_stripe_price(stripe_product_id, price)

        # Создаем сессию оплаты
        success_url = "http://127.0.0.1:8000/payment/success/"
        cancel_url = "http://127.0.0.1:8000/payment/cancel/"
        session = create_stripe_checkout_session(stripe_price_id, success_url, cancel_url)

        # Создаем запись в модели Payment
        payment = Payment.objects.create(
            user=user,
            course=course,
            amount=price / 100,  # Преобразуем цену обратно в рубли
            payment_method="stripe",
            stripe_product_id=stripe_product_id,
            stripe_price_id=stripe_price_id,
            stripe_session_id=session["id"],
            stripe_checkout_url=session["url"],
        )

        return Response({"checkout_url": session["url"]})
