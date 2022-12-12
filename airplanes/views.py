from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet

from airplanes.models import Airplane
from airplanes.serializers import AirplaneSerializer


class AirplaneViewSet(
    viewsets.ModelViewSet,
):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
