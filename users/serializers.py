from django.contrib.auth import get_user_model
from rest_framework import serializers

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
