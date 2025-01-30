from django.core.management.base import BaseCommand
from django.db.models import Sum
from rating_app.models import Post

class Command(BaseCommand):
    help = "Updates the average rating parameters every 1 week."
    
    def handle(self, *args, **kwargs):
        posts = Post.objects.all()

        for post in posts:
            C = post.reviews.count() # set C equal to number of reviews so far
            M = post.avg_rating # set M equal to current average rating
            SumR = post.reviews.aggregate(Sum('rating'))['rating__sum'] or 0 # total rating sum 
            N = post.reviews.count() # rating_count
            
            average_rating = (((C * M) + SumR) / (C + N)) if N > 0 else 0
            
            post.avg_rating = average_rating
            
            post.save()

        self.stdout.write(self.style.SUCCESS('Successfully updated parameters of weighted average!'))
