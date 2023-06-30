from django.contrib.auth.models import User
from .models import Post
from locations.models import Location
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_posts(self):
        adam = User.objects.get(username='adam')
        Post.objects.create(owner=adam, title='a title', name='luigi')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/posts/', {'title': 'a title', 'name': 'luigis'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_in_user_can_create_location(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post(
            '/posts/', {'title': 'a title', 'name': 'luigis'})
        count = Location.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        response = self.client.post(
            '/posts/', {'title': 'a title', 'name': 'luigis'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Post.objects.create(
            owner=adam, title='a title', name='luigis', content='adams content'
        )
        Post.objects.create(
            owner=brian, title='another title',
            name='maroks', content='brians content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.data['name'], 'luigis')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put(
            '/posts/1/', {'title': 'a new title', 'name': 'luigis'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
