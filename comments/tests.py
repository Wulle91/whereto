from django.test import TestCase
from django.contrib.auth.models import User
from posts.models import Post
from likes.models import Like
from rest_framework.test import APIClient
from rest_framework import status


class LikeTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username='user1', password='pass')
        self.user2 = User.objects.create_user(
            username='user2', password='pass')
        self.post = Post.objects.create(
            title='Test Post', content='Test Content', owner=self.user1)

    def test_authenticated_user_can_like_post(self):
        self.client.login(username='user1', password='pass')
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

    def test_unauthenticated_user_cannot_like_post(self):
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_delete_own_like(self):
        self.client.login(username='user1', password='pass')
        like = Like.objects.create(owner=self.user1, post=self.post)
        response = self.client.delete(f'/likes/{like.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(pk=like.id).exists())
