from django.db import models
from django.contrib.auth import get_user_model
# from django.urls import reverse


from apps. airplane. models import Airplane


User = get_user_model ()


class AirplaneComment (models.Model):
    user = models. ForeignKey (
        to=User,
        on_delete=models. CASCADE,
        related_name='comments'
    )
    airplane = models. ForeignKey(
        to=Airplane,
        on_delete=models.CASCADE,
        related_name= 'airplanes_comments'
    )
    comment_text = models. TextField ()
    created_at = models. DateTimeField (auto_now_add=True)
    
    def str(self) :
        return f'Comment from {self.user.username} to {self.airplane.title}'
    

class AirplaneRating (models.Model) :
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE =5
    RATING_CHOICES = (
        (ONE,'1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR,'4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    airplane = models. ForeignKey (
        to=Airplane, 
        on_delete=models.CASCADE, 
        related_name= 'airplanes_ratings'
    )

    def _str_ (self) -> str:
        return f'{self.rating} points to {self.airplane.title}'
    
    class Meta:
        unique_together = ['user', 'airplane', 'rating']

    
class AirplaneLike(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE, 
        related_name= 'likes'
    )
    airplane = models.ForeignKey(
    to=Airplane, 
    on_delete=models.CASCADE, 
    related_name= 'airplanes_likes'
    )

    def _str__(self) :
        return f'Liked by {self.user. username}'
    

class SavedAirplane(models.Model):
    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
    )
    airplane = models. ForeignKey (
    to=Airplane, 
    on_delete=models. CASCADE,
    )
