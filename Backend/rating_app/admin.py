from django.contrib import admin
from .models import Post, Review

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at', 'updated_at')
    search_fields = ('title', 'description')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'rating', 'description', 'created_at', 'updated_at')
    search_fields = ('post__title', 'user__username', 'description')
