from django.urls import path, include
from rest_framework import routers

from airplanes.views import AirplaneViewSet

router = routers.DefaultRouter()
router.register("airplanes", AirplaneViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airplanes"
