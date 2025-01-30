from django.core.management.base import BaseCommand
from django.db.models import Sum
from rating_app.models import Post

class Command(BaseCommand):
    help = "Updates the average rating of posts every 1 second."
    
    def handle(self, *args, **kwargs):
        posts = Post.objects.all()

        for post in posts:
            C = post.number_of_ratings_weekly
            M = post.avg_rating_weekly
            SumR = post.reviews.aggregate(Sum('rating'))['rating__sum'] or 0 # total rating sum 
            N = post.reviews.count() # rating_count
            
            average_rating = (((C * M) + SumR) / (C + N)) if N > 0 else 0
            
            post.avg_rating = average_rating
            
            post.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated average ratings for all posts.'))
