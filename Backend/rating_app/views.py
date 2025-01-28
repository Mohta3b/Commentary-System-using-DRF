from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, ReviewSerializer
from .models import *
from rest_framework.response import Response

# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
        
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
     
    
    def post_review(self):
        post = Post.objects.get(id=self.post_id)
        Review.objects.filter(post=post, user=self.user).delete()
        post.rating_set.create(user=self.user, rating=self.rating)
        return get_posts_list()
        
            
