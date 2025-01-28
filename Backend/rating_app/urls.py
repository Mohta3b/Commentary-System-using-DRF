from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, ReviewViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'reviews', ReviewViewSet, basename='review')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Custom endpoint for adding/updating reviews
    path('reviews/review/', ReviewViewSet.as_view({'post': 'review'}), name='review'),
]
