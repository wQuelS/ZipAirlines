from typing import Dict, Any

from django.conf import settings
from rest_framework import serializers

from airplanes.models import Airplane
from airplanes.airplane_utility import AirplaneUtility


class AirplaneSerializer(serializers.ModelSerializer):
    tank_capacity = serializers.SerializerMethodField()
    consumption_per_minute = serializers.SerializerMethodField()
    minutes_to_fly = serializers.SerializerMethodField()
    airline = serializers.SerializerMethodField()

    def get_airline(self, obj: Airplane) -> str:
        return obj.airline.name

    class Meta:
        model = Airplane
        fields = (
            "id",
            "airline",
            "passengers",
            "capacity",
            "tank_capacity",
            "consumption_per_minute",
            "minutes_to_fly",
        )
        read_only_fields = (
            "consumption_per_minute",
            "minutes_to_fly",
            "fuel_tank",
        )

    def get_tank_capacity(self, plane: Airplane) -> int:
        return AirplaneUtility(plane).tank_capacity

    def get_consumption_per_minute(self, plane: Airplane) -> float:
        return AirplaneUtility(plane).consumption_per_minute

    def get_minutes_to_fly(self, plane: Airplane) -> float:
        return AirplaneUtility(plane).minutes_to_fly


class AirplaneCreateSerializer(AirplaneSerializer):
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if Airplane.objects.count() >= 10:
            raise serializers.ValidationError(
                "Cannot create more than 10 airplanes."
            )

        return data


class AirlineSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=100, required=False)
    airplanes = AirplaneSerializer(
        many=True, max_length=settings.MAX_PLANES, required=False
    )

    class Meta:
        fields = (
            "id",
            "name",
            "airplanes",
        )

    def get_airplanes(self, airline: Airplane) -> Airplane:
        # Return the queryset of airplanes for the given airline
        return Airplane.objects.filter(airline=airline)
