from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from materials.models import Course
from users.models import User


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(id=1, email='user@test.ru',
                                        password='12345', )
        self.client.force_authenticate(user=self.user)

        """Создание тестового курса"""
        self.course = Course.objects.create(name='test_course',
                                            description='test_description')

        """Ссылка на контроллер управления подпиской"""
        self.path = reverse('users:sub_switch', [self.course.id])

    def test_sub_on(self):
        """Тестрование добавления подписки (однократное
           обращение к контроллеру)"""
        response = self.client.post(self.path)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Подписка добавлена")

    def test_sub_off(self):
        """Тестрование удаления подписки (двойное
           обращение к контроллеру)"""
        response = self.client.post(self.path)
        response = self.client.post(self.path)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Подписка удалена")
