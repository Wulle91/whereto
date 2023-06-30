
from django.contrib.auth.models import User
from .models import Location
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_locations(self):
        adam = User.objects.get(username='adam')
        Location.objects.create(name='luigis')
        response = self.client.get('/locations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_location(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/locations/', {'name': 'luigis', 'address': 'some'})
        count = Location.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_location(self):
        response = self.client.post('/locations/', {'name': 'luigis', 'address': 'some'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
