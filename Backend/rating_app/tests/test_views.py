from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from rating_app.models import Post, Review

User = get_user_model()

class PostViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.post = Post.objects.create(title="Test Post", description="This is a test post")
       

    def addNewPost(self):
        Post.objects.create(title="Test Post 2", description="This is a test post 2")
        
    def test_list_posts_single_post(self):
        """Ensure posts are listed properly"""
        response = self.client.get("/posts/")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Post")
        
    def test_list_posts_multiple_posts(self):
        """Ensure posts are listed properly"""
        self.addNewPost()
        response = self.client.get("/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Test Post")
        self.assertEqual(response.data[1]["title"], "Test Post 2")


class ReviewViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.post = Post.objects.create(title="Test Post", description="This is a test post")
        self.client.login(username="testuser", password="testpass")
        self.review_url = "/reviews/review/"

    def test_add_review(self):
        """Ensure a review can be added"""
        data = {
            "post_id": self.post.id,
            "rating": 5,
            "description": "Great post!"
        }
        response = self.client.post(self.review_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_rating"], 5)

    def test_review_requires_authentication(self):
        """Ensure unauthenticated users cannot add a review"""
        self.client.logout()
        data = {
            "post_id": self.post.id,
            "rating": 4,
            "description": "Nice!"
        }
        response = self.client.post(self.review_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
