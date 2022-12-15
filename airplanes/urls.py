from django.urls import path, include
from rest_framework import routers

from airplanes.views import AirplaneViewSet, fleet

router = routers.DefaultRouter()
router.register("airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("airline/", fleet, name="airlines"),
]

app_name = "airplanes"
