from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from materials.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(id=1, email='user@test.ru', password='12345')
        self.client.force_authenticate(user=self.user)
        """Создание тестовых курса и урока"""
        self.course = Course.objects.create(name='test_course', description='test_description')
        self.lesson = Lesson.objects.create(name='test_lesson', description='test_description',
                                            course=self.course, url='https://test.youtube.com/',
                                            owner=self.user)

    def test_create_lesson(self):
        """Тестирование создания урока"""
        data = {'name': 'Creating_test', 'description': 'Creating_test',
                'course': self.course.id, 'url': 'https://test.youtube.com/',
                'owner': self.user.id}
        response = self.client.post('/lesson/create/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name=data['name']).exists())

    def test_retrieve_lesson(self):
        """Тестирование просмотра информации об уроке"""
        path = reverse('materials:lesson_view', [self.lesson.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        path = reverse('materials:lesson_update', [self.lesson.id])
        data = {'name': 'Updating_test', 'description': 'Updating_test'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, data['name'])

    def test_delete_lesson(self):
        moderator = User.objects.create(id=2, email='moderator@mail.ru',
                                        password='qwerty', role='moderator')
        self.client.force_authenticate(user=moderator)

        path = reverse('materials:lesson_delete', [self.lesson.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
