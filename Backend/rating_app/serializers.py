from rest_framework import serializers
from .models import Post, Review

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
    class Meta:
        model = Review
        fields = ['id', 'post', 'user', 'rating', 'description', 'created_at', 'updated_at']
        
        def create(self, validated_data):
            post_id = self.context['post_id']
            user_id = self.context['user_id']
            if not post_id or not user_id:
                raise serializers.ValidationError("post_id and user_id must be provided in the context.")
              
            review = Review.objects.create(post_id= post_id, user_id=user_id, **validated_data)
            return review