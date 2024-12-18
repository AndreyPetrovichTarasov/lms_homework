from rest_framework import serializers

from users.models import Payment

from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уроков.
    """

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курсов.
    """

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "name", "description", "lessons_count", "lessons", "owner"]

    def get_lessons_count(self, instance):
        """
        Получение количество уроков.
        """
        return instance.lessons.count()


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
