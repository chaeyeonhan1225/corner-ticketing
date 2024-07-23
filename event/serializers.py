from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from event.models import Event


class EventSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    representative_price = serializers.IntegerField(source='min_price')

    class Meta:
        model = Event
        fields = "__all__"