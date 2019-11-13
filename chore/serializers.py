from rest_framework import serializers

from chore.models import RentalPeriod


class RentalPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentalPeriod
        fields = ['id', 'start_datetime', 'end_datetime']
