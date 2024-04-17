from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.test import force_authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from materials.models import Course, Lesson, Subscription
from users.models import User
from rest_framework.test import APIClient


class LessonTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            email="test4@test4.ru",
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.user.set_password("test")
        self.user.save()

        self.course = Course.objects.create(
            name='Test',
            description='Test',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='Test',
            description='Test_lesson',
            owner=self.user
        )

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {
            "name": "Test8 Django",
            "description": "Test8",
            "url": "https://www.youtube.com/watch?v=N2acITrfzHQ",
            "course": "1"
        }

        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], data['name'])


    def test_create_lesson_validation_error(self):
        """Тестирование создания урока"""
        data = {
            "name": "Test9 Django",
            "description": "Test9",
            "url": "https://rutube.ru/video/8dfjt5j4j7dfi3/",
            "course": "1"
        }

        response = self.client.post(
            reverse('materials:lesson-create'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Нельзя использовать ссылки на сторонние сайты']})


    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(
            reverse('materials:lesson-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['name'], self.lesson.name)


    def test_retrieve_lesson(self):
        """Тестирование вывода одного урока"""
        response = self.client.get(
            reverse('materials:lesson-get', args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)


    def test_update_lesson(self):
        """Тестирование обновления урока"""
        updated_data = {
            "description": "Updated lesson",
            "url": "https://www.youtube.com/watch?v=N2acITrfzHQ"
        }

        response = self.client.patch(
            reverse('materials:lesson-update', args=[self.lesson.id]), updated_data
        )

        self.lesson.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], updated_data['description'])


    def test_delete_lesson(self):
        """Тестирование удаления урока"""
        response = self.client.delete(
            reverse('materials:lesson-delete', args=[self.lesson.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            email="test4@test4.ru",
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        self.user.set_password("test")
        self.user.save()

        self.course = Course.objects.create(
            name='Test',
            description='Test',
            owner=self.user
        )

        self.subscribe = Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_subscribe_to_course(self):
        """Тестирование функционала подписки на курс"""
        data = {
            "user": self.user,
            "course": self.course.id
        }

        response = self.client.post(
            reverse('materials:subscription'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')

    def test_unsubscribe_to_course(self):
        """Тестирование функционала подписки на курс"""
        data = {
            "user": self.user,
            "course": self.course.id
        }

        response = self.client.post(
            reverse('materials:subscription'),
            data=data
        )
        response = self.client.post(
            reverse('materials:subscription'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
