import unittest
from rest_framework.serializers import ValidationError
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from lms.models import Course, Lesson, Subscription
from .validators import YouTubeLinkValidator


class YouTubeLinkValidatorTestCase(unittest.TestCase):
    def setUp(self):
        self.validator = YouTubeLinkValidator(field='material_link')

    def test_valid_youtube_link(self):
        data = {'material_link': 'https://www.youtube.com/watch?v=abc123'}
        try:
            self.validator(data)
        except ValidationError:
            self.fail('ValidationError raised for valid YouTube link')

    def test_invalid_udemy_link(self):
        data = {'material_link': 'https://www.udemy.com/course/python'}
        with self.assertRaises(ValidationError):
            self.validator(data)

    def test_invalid_personal_site(self):
        data = {'material_link': 'https://myblog.ru/video'}
        with self.assertRaises(ValidationError):
            self.validator(data)

    def test_empty_link(self):
        data = {'material_link': ''}
        try:
            self.validator(data)
        except ValidationError:
            self.fail('ValidationError raised for empty link')

    def test_missing_field(self):
        data = {}
        try:
            self.validator(data)
        except ValidationError:
            self.fail('ValidationError raised for missing field')


class LessonAndSubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Пользователи
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='pass'
        )
        self.other_user = User.objects.create_user(
            username='other',
            email='other@example.com',
            password='pass'
        )

        # Курс и урок
        self.course = Course.objects.create(owner=self.owner, title='Test Course', description='...')
        self.lesson = Lesson.objects.create(
            owner=self.owner,
            course=self.course,
            title='Test Lesson',
            description='...',
            video_url='https://youtube.com/watch?v=test'
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'Some text',
            'video_url': 'https://youtube.com/watch?v=new'
        }
        response = self.client.post('/api/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lesson(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.lesson.title)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.owner)
        data = {'title': 'Updated Title'}
        response = self.client.patch(f'/api/lessons/{self.lesson.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post('/api/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка добавлена')
        self.assertTrue(Subscription.objects.filter(user=self.other_user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.other_user, course=self.course)
        self.client.force_authenticate(user=self.other_user)
        response = self.client.post('/api/subscribe/', {'course_id': self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'подписка удалена')
        self.assertFalse(Subscription.objects.filter(user=self.other_user, course=self.course).exists())
