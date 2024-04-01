from rest_framework.routers import DefaultRouter

from .views import (
    ProducerViewSet, 
    AirplaneViewSet,
    TypeViewSet  
    )

router = DefaultRouter()
router.register('producer', ProducerViewSet)
router.register('airplane', AirplaneViewSet)
router.register('type', TypeViewSet) 

urlpatterns = [

]

urlpatterns += router.urls