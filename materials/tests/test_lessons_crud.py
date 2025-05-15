from urllib import response

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, MODERATOR_GROUP_NAME
from materials.models import Lesson, Course
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile

MODERATOR_GROUP_NAME = 'Модераторы'


class LessonCRUDTest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create(email='test@email.com', password='qwerty')
        self.moderator = User.objects.create(email='moderator@email.com', password='qwerty')

        moderator_group = Group.objects.create(name=MODERATOR_GROUP_NAME)
        self.moderator.groups.add(moderator_group)

        self.course = Course.objects.create(name='Test Course', owner=self.owner)
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Lesson',
            link_to_the_video='https://youtube.com/watch?v=123',
            course=self.course,
            owner=self.owner,
        )

    def test_create_lesson_owner(self):
        "Создание урока владельцем"
        self.client.force_authenticate(user=self.owner)
        url = reverse('materials:lesson-create')

        from io import BytesIO
        from PIL import Image

        image = Image.new('RGB', (1, 1), color='red')
        image_io = BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)

        dummy_image = SimpleUploadedFile(
            name='test_image.png',
            content=image_io.read(),
            content_type='image/png'
        )

        data = {
            'name': 'Test Lesson 2',
            'description': 'Test Lesson 2',
            'link_to_the_video': 'https://youtube.com/watch?v=123',
            'course': self.course.id,
            'preview': dummy_image,
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson_owner(self):
        "Обновление урока владельцем"
        self.client.force_authenticate(user=self.owner)
        url = reverse('materials:lesson-update', kwargs={'pk': self.lesson.pk})
        data = {'name': 'UPD Lesson name'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'UPD Lesson name')

    def test_delete_lesson_owner(self):
        "Удаление урока владельцем"
        self.client.force_authenticate(user=self.owner)
        url = reverse('materials:lesson-destroy', kwargs={'pk': self.lesson.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_list_lessons_for_owner(self):
        """Владелец видит только свои уроки."""
        self.client.force_authenticate(user=self.owner)
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

