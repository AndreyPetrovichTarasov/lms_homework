from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для уроков.
    """

    video_url = serializers.URLField(validators=[YouTubeLinkValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для курсов.
    """

    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    video_url = serializers.URLField(validators=[YouTubeLinkValidator()])
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "lessons_count",
            "lessons",
            "video_url",
            "owner",
            "is_subscribed",
        ]

    def get_lessons_count(self, instance):
        """
        Получение количество уроков.
        """
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
