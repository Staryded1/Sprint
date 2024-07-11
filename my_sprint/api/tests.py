from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import PerevalAdded, User
from .serializers import PerevalAddedSerializer
import json

class SubmitDataViewTests(APITestCase):

    def setUp(self):
        # Создаем пользователя для тестов
        self.user = User.objects.create(
            email='testuser@example.com',
            fam='Test',
            name='User',
            otc='Tester',
            phone='1234567890'
        )
        
        # Создаем запись PerevalAdded для тестов
        self.pereval = PerevalAdded.objects.create(
            user=self.user,
            beauty_title='Test Title',
            title='Test Title',
            other_titles='Other Title',
            connect='Test Connect',
            add_time='2024-06-25T14:30:00Z',
            status='new'
        )

    def test_get_list(self):
        # Тестируем получение списка записей по email пользователя
        url = reverse('submit_data')  # Замените на имя URL, если используется имя
        response = self.client.get(url, {'user__email': self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.pereval.title)

    def test_get_detail(self):
        # Тестируем получение отдельной записи по ID
        url = reverse('submit_data_detail', args=[self.pereval.id])  # Замените на имя URL, если используется имя
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.pereval.title)

    def test_post(self):
        # Тестируем создание новой записи
        url = reverse('submit_data')  # Замените на имя URL, если используется имя
        data = {
            "user": self.user.id,
            "beauty_title": "New Title",
            "title": "New Title",
            "other_titles": "Other Titles",
            "connect": "New Connect",
            "add_time": "2024-06-25T14:30:00Z",
            "status": "new"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PerevalAdded.objects.count(), 2)
        self.assertEqual(PerevalAdded.objects.get(id=response.data['id']).title, "New Title")

    def test_patch(self):
        # Тестируем обновление существующей записи
        url = reverse('submit_data_detail', args=[self.pereval.id])  # Замените на имя URL, если используется имя
        data = {
            "beauty_title": "Updated Title"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], 1)
        self.assertEqual(PerevalAdded.objects.get(id=self.pereval.id).beauty_title, "Updated Title")

    def test_patch_invalid_status(self):
        # Тестируем обновление записи с неподходящим статусом
        self.pereval.status = 'processed'
        self.pereval.save()
        
        url = reverse('submit_data_detail', args=[self.pereval.id])  # Замените на имя URL, если используется имя
        data = {
            "beauty_title": "Updated Title"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['state'], 0)
        self.assertEqual(response.data['message'], 'Cannot update record that is not in new status')

