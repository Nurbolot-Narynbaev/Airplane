from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SavedAirplaneViewSet,
    AirplaneCommentView,
    RatingView,
    LikeView,
)


router = DefaultRouter()


router.register('saved-airplane',SavedAirplaneViewSet, 'saved airplane' )
router.register ('airplane-comment', AirplaneCommentView, 'comment')
router.register( 'airplane-rating', RatingView, 'rating')
router.register( 'airplane-like', LikeView, 'like')


urlpatterns = [

]
urlpatterns += router.urls

