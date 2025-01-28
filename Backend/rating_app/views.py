from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import PostSerializer, ReviewSerializer

# Create your views here.
class PostViewSet(ModelViewSet):
    queryset = ModelViewSet.objects.all()
    serializer_class = PostSerializer
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def 
