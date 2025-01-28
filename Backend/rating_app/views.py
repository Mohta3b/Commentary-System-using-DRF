from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, ReviewSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils.timezone import now

# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
    
class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
     
    
    def review(self, request, *args, **kwargs):
        post_id = request.data.get('post_id')
        rating = request.data.get('rating')
        description = request.data.get('description', '')

        if not post_id or rating is None:
            return Response({"error": "post_id and rating are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the user has already reviewed this post
        review, created = Review.objects.get_or_create(post=post, user=request.user, defaults={
            'rating': rating,
            'description': description,
        })

        if not created:
            # Update rating, description and updated_at fields
            review.rating = rating
            review.description = description
            review.updated_at = now()
            review.save()

        # # if in some cases we need to have average_rating filed in the model, then we need to update it here
        # average_rating = Review.objects.filter(post=post).aggregate(models.Avg('rating'))['rating__avg'] or -1
        # post.average_rating = average_rating
        # post.save()
        
        response_data = {
            "post_id": post.id,
            "user_rating": rating,
            "average_rating": post.average_rating(),  
            "updated_at": post.updated_at.isoformat()
        }
        
        return Response(response_data, status=status.HTTP_200_OK)

        # # if we want to update the whole screen just by rating, we can use this piece of code!
        # posts = Post.objects.all()
        # post_serializer = PostSerializer(posts, many=True, context={'request': request})
        # return Response(post_serializer.data, status=status.HTTP_200_OK)
        
            
