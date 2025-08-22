from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from django.db.models import Count, Avg

class Meal(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=32)
    description = models.TextField(max_length=360)

    def ratings_count(self):
        c= Rating.objects.filter(meal=self).aggregate(Count('stars'))["stars__count"]
        return c

    def avg_ratings(self):
        a= Rating.objects.filter(meal=self).aggregate(Avg('stars'))["stars__avg"]
        return a

    def __str__(self):
        return self.title


class Rating(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

    def __str__(self):
        return str(self.stars)
    
    class Meta:
        unique_together = (('user', 'meal'),) # a User can't rate the same Meal twice