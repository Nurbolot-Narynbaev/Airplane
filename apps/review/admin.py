from django.contrib import admin
from .models import (
    AirplaneComment,
    AirplaneRating,
    AirplaneLike,
)


admin.site.register([AirplaneComment, AirplaneRating, AirplaneLike])