from rest_framework import serializers
from .models import Post, Review
from django.utils.timezone import now

from django.db.models import Sum

class PostSerializer(serializers.ModelSerializer):
    
    user_rating = serializers.SerializerMethodField()
    num_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'average_rating', 'user_rating', 'num_reviews']
        
    def get_user_rating(self, obj):
        request = self.context.get('request')
        if request:
            user_review = obj.reviews.filter(user=request.user).first()
            return user_review.rating if user_review else None
        return None

    def get_num_reviews(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        return obj.average_rating()
        
class ReviewSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'post', 'user', 'rating', 'description', 'created_at', 'updated_at']
        
        def validate_post_id(self, value):
            if not Post.objects.filter(id=value).exists():
                raise serializers.ValidationError("Post not found.")
            return value

        def create_or_update_review(self, user):
            post = Post.objects.get(id=self.validated_data['post_id'])
            review, created = Review.objects.get_or_create(
                post=post, user=user,
                defaults={'rating': self.validated_data['rating'], 'description': self.validated_data.get('description', '')}
            )

            if not created:
                review.rating = self.validated_data['rating']
                review.description = self.validated_data.get('description', '')
                review.updated_at = now()
                review.save()

            return review