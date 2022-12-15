from typing import Type

from django.db.migrations import serializer
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from airplanes.models import Airplane, Airline
from airplanes.serializers import (
    AirplaneSerializer,
    AirlineSerializer,
    AirplaneCreateSerializer,
)


class AirplaneViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Airplane.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "create":
            return AirplaneCreateSerializer
        return AirplaneSerializer


@api_view(["GET"])
def fleet(request) -> Response:
    airline = Airline.objects.get()
    request.data["airline"] = airline

    serializer = AirlineSerializer(data=request.data, instance=airline)

    if serializer.is_valid(raise_exception=True):
        return Response(serializer.data)
