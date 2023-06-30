from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from posts.models import Post
from likes.models import Like


class LikeTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username='user', password='pass')
        self.post = Post.objects.create(
            title='Post', content='test', owner=self.user)

    def test_create_like(self):
        self.client.login(username='user', password='pass')
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        like = Like.objects.get(pk=response.data['id'])
        self.assertEqual(like.owner, self.user)
        self.assertEqual(like.post, self.post)
        count = Like.objects.count()
        self.assertEqual(count, 1)

    def test_unauthenticated_user_cannot_like_post(self):
        response = self.client.post('/likes/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_delete_own_like(self):
        self.post = Post.objects.create(
            title='post', content='test', owner=self.user)
        self.like = Like.objects.create(owner=self.user, post=self.post)

        self.client.login(username='user', password='pass')
        response = self.client.delete(f'/likes/{self.like.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(pk=self.like.id).exists())
