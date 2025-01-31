from django.core.management import call_command
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User
from rating_app.models import Post, Review
from unittest.mock import patch
import time

# Tests are written for these scenarios:
    # Basic Scenario: Ensure the command runs correctly and updates average ratings for posts with no reviews.
    # Post with Reviews: Test posts that already have reviews and check that the average rating is updated correctly.
    # Multiple Posts: Ensure the command works with multiple posts, checking if each post’s average rating is updated.
    # Edge Case: Test when there are no posts in the database.
    # High Volume: Test with a large number of posts (simulate a large dataset).

class UpdateAverageRatingTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user2 = User.objects.create_user(username="testuser1", password="testpass2")
        
        # Create posts with no reviews (basic scenario)
        self.post_no_reviews = Post.objects.create(title="Post No Reviews", description="Test Post with no reviews")
        
        # Create posts with reviews
        self.post_with_reviews = Post.objects.create(title="Post With Reviews", description="Test Post with reviews")
        Review.objects.create(post=self.post_with_reviews, user=self.user, rating=4)
        Review.objects.create(post=self.post_with_reviews, user=self.user2, rating=5)

    def test_command_updates_average_rating_no_reviews(self):
        """Test the command with posts that have no reviews"""
        # Before running the command, avg_rating should be 0
        self.assertEqual(self.post_no_reviews.avg_rating, 0)
        
        call_command('update_average_ratings')
        
        # After running the command, avg_rating should still be 0 as there are no reviews
        self.assertEqual(self.post_no_reviews.avg_rating, 0)

    def test_command_updates_average_rating_with_reviews(self):
        """Test the command with posts that have reviews"""
        # Before running the command, calculate the expected average for the post with reviews
        expected_avg = (4 + 5) / 2  # simple average of 4 and 5
        
        call_command('update_average_ratings')
        
        self.post_with_reviews.refresh_from_db()
        
        # After running the command, avg_rating should be updated correctly
        self.assertEqual(self.post_with_reviews.avg_rating, expected_avg)

    def test_command_handles_multiple_posts(self):
        """Test the command with multiple posts"""
        post_1 = Post.objects.create(title="Post 1", description="Test Post 1", avg_rating_weekly=3, number_of_ratings_weekly=2)
        post_2 = Post.objects.create(title="Post 2", description="Test Post 2", avg_rating_weekly=4, number_of_ratings_weekly=1)
        
        Review.objects.create(post=post_1, user=self.user, rating=3)
        Review.objects.create(post=post_2, user=self.user, rating=5)
        
        call_command('update_average_ratings')
        
        post_1.refresh_from_db()
        post_2.refresh_from_db()
        
        first_expected_result = ((3*2) + 3) / (2+1)
        second_expected_result = ((4*1) + 5) / (1+1)
        
        self.assertEqual(post_1.avg_rating, first_expected_result)
        self.assertEqual(post_2.avg_rating, second_expected_result)

    def test_command_edge_case_no_posts(self):
        """Test the command with no posts in the database"""
        Post.objects.all().delete()  # Remove all posts
        
        # Run the command, should not throw errors
        call_command('update_average_ratings')
        
        # There should be no posts left
        self.assertEqual(Post.objects.count(), 0)

    def test_command_high_volume(self):
        """Test the command with a large number of posts"""
        Post.objects.all().delete()
        POSTS_NUM = 1000
        for i in range(POSTS_NUM):
            post = Post.objects.create(title=f"Post {i}", description=f"Test Post {i}", avg_rating_weekly=3, number_of_ratings_weekly=2)
            Review.objects.create(post=post, user=self.user, rating=4)
        
        call_command('update_average_ratings')
        
        expected_result = ((3*2) + 4) / (2+1)
        
        posts = Post.objects.all()
        for post in posts:
            post.refresh_from_db()
            self.assertEqual(post.avg_rating, expected_result)

    @patch('rating_app.management.commands.update_average_ratings.Post.objects.all')
    def test_command_mocked(self, mock_posts):
        """Test with mocked posts for performance or edge case scenarios"""
        # Mock the posts returned by the database query
        mock_posts.return_value = [self.post_no_reviews, self.post_with_reviews]
        
        call_command('update_average_ratings')
        
        self.assertEqual(self.post_no_reviews.avg_rating, 0)
        self.assertEqual(self.post_with_reviews.avg_rating, 4.5)  # Average of 4 and 5
