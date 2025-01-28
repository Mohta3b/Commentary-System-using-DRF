from rest_framework_nested import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()

router.register("posts", views.PostViewSet)

post_router = routers.NestedDefaultRouter(router, "posts", lookup='post')
post_router.register("reviews", views.ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(post_router.urls)),
]