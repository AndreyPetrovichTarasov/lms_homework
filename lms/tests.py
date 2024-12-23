from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson, Subscription
from rest_framework.reverse import reverse


class LessonTests(APITestCase):
    def setUp(self):
        # Создание пользователя
        self.user = get_user_model().objects.create_user(
            email="email@email.com", password="testpassword"
        )

        # Создание курса
        self.course = Course.objects.create(
            name="Test Course", description="Test Description", owner=self.user
        )

        # Создание урока
        self.lesson = Lesson.objects.create(
            name="Test Lesson",
            video_url="http://youtube.com/test",
            course=self.course
        )

        # Подготовка URL
        self.lesson_url = reverse('lms:lesson-detail', kwargs={'pk': self.lesson.pk})
        self.lesson_list_url = reverse('lms:lesson-list')
        self.lesson_create_url = reverse('lms:lesson-create')

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        data = {
            'name': 'New Lesson',
            'video_url': 'http://youtube.com/newvideo',
            'course': self.course.id,
        }
        response = self.client.post(reverse('lms:lesson-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(self.lesson_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        response = self.client.delete(reverse('lms:lesson-delete', kwargs={'pk': self.lesson.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_get_lesson(self):
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Lesson')
        self.assertEqual(response.data['video_url'], 'http://youtube.com/test')

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.user)  # Аутентификация пользователя
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Мы ожидаем один урок
        self.assertEqual(response.data[0]['name'], 'Test Lesson')
        self.assertEqual(response.data[0]['video_url'], 'http://youtube.com/test')


class SubscriptionTests(APITestCase):
    def setUp(self):
        # Создание пользователей
        self.user1 = get_user_model().objects.create_user(
            email="email@email.com", password="testpassword1"
        )
        self.user2 = get_user_model().objects.create_user(
            email="email2@email.com", password="testpassword2"
        )

        # Создание курса
        self.course = Course.objects.create(name="Test Course", description="Test Description", owner=self.user1)

        # Подготовка URL для подписки
        self.subscribe_url = reverse('lms:subscribe')

    def test_subscribe(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user2)
        data = {"course_id": self.course.id}

        # Проверка добавления подписки
        response = self.client.post(self.subscribe_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsubscribe(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user2)
        data = {"course_id": self.course.id}

        # Добавляем подписку
        self.client.post(self.subscribe_url, data, format='json')

        # Проверка удаления подписки
        response = self.client.post(self.subscribe_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertEqual(Subscription.objects.count(), 0)

    def test_subscribe_without_course_id(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user2)

        # Проверка ошибки при отсутствии `course_id`
        response = self.client.post(self.subscribe_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'course_id is required')

    def test_subscribe_with_invalid_course(self):
        # Аутентификация пользователя
        self.client.force_authenticate(user=self.user2)

        # Проверка подписки на несуществующий курс
        data = {"course_id": 9999}  # Неверный ID курса
        response = self.client.post(self.subscribe_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
