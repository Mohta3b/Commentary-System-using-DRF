from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, default="Content-Title")
    description = models.TextField()

    def average_rating(self) -> float:
        return Review.objects.filter(post=self).aggregate(Avg("rating"))["rating__avg"] or -1

    def __str__(self):
        return f"{self.title}: {self.average_rating()}"
    

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=-1, choices=((0, '0 score'), (1, '1 score'), (2, '2 score'), (3, '3 score'), (4, '4 score'), (5, '5 score'))) 
    
    class Meta:
        unique_together = ('post', 'user')
    
    def __str__(self):
        return f"{self.post.title}: {self.rating}"