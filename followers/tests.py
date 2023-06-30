from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Follower
from locations.models import Location
from django.db import transaction


class FollowerTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(username='user1', password='123')
        self.user2 = User.objects.create_user(username='user2', password='123')
        self.location = Location.objects.create(
            name='Location 1', address='Address 1')

    def tearDown(self):
        Follower.objects.all().delete()

    def test_logged_in_user_can_follow(self):
        self.client.login(username='user1', password='123')
        data = {'followed': self.user2.id,
                'followed_location': self.location.id}
        response = self.client.post('/followers/', data, format='json')

        count = Follower.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        follower = Follower.objects.first()
        self.assertEqual(follower.owner, self.user1)
        self.assertEqual(follower.followed, self.user2)
        self.assertEqual(follower.followed_location, self.location)

    def test_cannot_create_duplicate_follower(self):
        self.client.login(username='user1', password='123')

        data = {'followed': self.user2.id,
                'followed_location': self.location.id}
        response = self.client.post('/followers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        with transaction.atomic():
            response = self.client.post('/followers/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Follower.objects.count(), 1)
