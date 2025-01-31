from django.test import TestCase
from rating_app.serializers import PostSerializer, ReviewSerializer
from rating_app.models import Post, Review
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

User = get_user_model()

class PostSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.post = Post.objects.create(title="Test Post", description="Test Description")

    def test_post_serializer(self):
        """Test serialization of post data"""
        factory = APIRequestFactory()
        request = factory.get('/posts/')
        request.user = self.user

        # Add the request to the context when instantiating the serializer
        serializer = PostSerializer(instance=self.post, context={'request': request})
        data = serializer.data
        
        self.assertEqual(data["title"], "Test Post")
        self.assertEqual(data["description"], "Test Description")
        self.assertIn("average_rating", data)

class ReviewSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.post = Post.objects.create(title="Test Post", description="Test Description")
        self.review = Review.objects.create(post=self.post, user=self.user, rating=5, description="Nice Post")

    def test_review_serializer(self):
        """Test serialization of review data"""
        serializer = ReviewSerializer(instance=self.review)
        data = serializer.data
        self.assertEqual(data["rating"], 5)
        self.assertEqual(data["description"], "Nice Post")
