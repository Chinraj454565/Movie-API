from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.

class StreamPlatform(models.Model):
    name=models.CharField(max_length=30)
    about=models.CharField(max_length=150)
    website=models.URLField(max_length=100)
    
    
    def __str__(self):
        return self.name


class WatchList(models.Model):
    title=models.CharField(max_length=50)
    stotyline=models.CharField(max_length=200)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    avg_rating=models.FloatField(default=0)#both shoulf 0 when creating new watchlist obj
    number_rating=models.IntegerField(default=0)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE, related_name="watch_list")
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    rating=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description=models.CharField(max_length=200, null=True)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now=True)
    watchlist=models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name="reviews")
    review_user=models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.rating)+" | "+self.watchlist.title