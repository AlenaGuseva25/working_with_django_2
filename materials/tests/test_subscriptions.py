from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from materials.models import Course, Subscription


class SubscriptionsTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user@sobaka.com', password='<sobaka>')
        self.course = Course.objects.create(name='Test Course', owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe_success(self):
        "Тест возможности подписаться"
        url = reverse('materials:course-subscribe', kwargs={'pk': self.course.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())


    def test_unsubscribe_success(self):
        "Тест возможности отписки"
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse('materials:course-unsubscribe', kwargs={'pk': self.course.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.exists())

    def test_is_unsubscribe_field(self):
        "Проверка поля is_subscribed на корректность"
        url = reverse('materials:course-detail', kwargs={'pk': self.course.pk})

        response = self.client.get(url, format='json')
        self.assertFalse(response.data.get('is_subscribed'))

        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.get(url, format='json')
        self.assertTrue(response.data.get('is_subscribed'))
