from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet

from users.models import Payment
from .filters import PaymentFilter
from .models import Course
from .serializers import CourseSerializer, PaymentSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Lesson
from .serializers import LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD операций с курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonListCreateAPIView(ListCreateAPIView):
    """
    ListCreateAPIView для получения списка уроков и создания нового урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    RetrieveUpdateDestroyAPIView для получения, обновления и удаления урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class PaymentViewSet(ModelViewSet):
    """
    ViewSet для работы с платежами.
    """
    queryset = Payment.objects.select_related('user', 'course', 'lesson')
    serializer_class = PaymentSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['date']
    ordering = ['-date']
