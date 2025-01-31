from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, ReviewSerializer
from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action


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
        
    @action(detail=False, methods=['post'])
    def review(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            review = serializer.create_or_update_review(request.user)
            post = review.post
        
            response_data = {
                "post_id": post.id,
                "user_rating": review.rating,
                "average_rating": post.average_rating(),  
                "updated_at": post.updated_at.isoformat()
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
            
