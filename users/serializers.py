from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import Payment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "city",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения пользователя.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "avatar",
            "city",
        ]
        read_only_fields = ["email"]


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    """

    user = serializers.StringRelatedField()
    course = serializers.StringRelatedField()
    lesson = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = ["id", "user", "date", "course", "lesson", "amount", "payment_method"]
