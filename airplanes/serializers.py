from rest_framework import serializers

from airplanes.models import Airplane


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "board_num",
            "passengers",
            "consumption_per_minute",
            "minutes_to_fly",
        )
        read_only_fields = ("consumption_per_minute", "minutes_to_fly")
