from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from users.permissions import IsModer, IsOwner

from .models import Course, Lesson, Subscription
from .paginators import CustomPageNumberPagination
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()


class LessonListAPIView(ListAPIView):
    """
    Получения списка уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination


class LessonCreateAPIView(CreateAPIView):
    """
    Создания урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Автоматическое добавление поля "Владелец" при создании.
        """
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    """
    Просмотр урокоа.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(UpdateAPIView):
    """
    Изменение урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(DestroyAPIView):
    """
    Удаление урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | IsModer)


class CourseUpdateAPIView(APIView):
    """
    Контроллер для обновления курса.
    """

    def put(self, request, *args, **kwargs):
        course_id = kwargs.get("pk")
        course = get_object_or_404(Course, id=course_id)

        # Обновление курса
        course.name = request.data.get("name", course.name)
        course.description = request.data.get("description", course.description)
        course.save()

        # Получение подписчиков курса
        subscriptions = Subscription.objects.filter(course=course)

        # Отправка писем подписчикам
        for subscription in subscriptions:
            send_course_update_email.delay(
                user_email=subscription.user.email,
                course_name=course.name,
                update_info="Курс обновлен. Проверьте новые материалы!",
            )

        return Response({"message": "Курс обновлен и уведомления отправлены"}, status=HTTP_200_OK)
