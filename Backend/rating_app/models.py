from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, default="Post-Title")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    avg_rating = models.FloatField(default=-1, editable=False) # -1 when no rating exists
    avg_rating_weekly = models.FloatField(default=0, editable=False)
    number_of_ratings_weekly = models.IntegerField(default=0, editable=False)

    def average_rating(self) -> float:
        return self.avg_rating
        # return Review.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or -1
    
    
    def __str__(self):
        return f"{self.title}: {self.average_rating()}"
    

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(
        default=-1,
        choices=[(i, f'{i} score') for i in range(6)],
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.post.title}: {self.rating}"