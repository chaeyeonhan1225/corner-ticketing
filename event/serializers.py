from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers

from event.models import Event


class EventSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    regular_price = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_regular_price(self, obj: Event):
        representative_ticket = obj.ticket_set.first()
        return representative_ticket.regular_price if representative_ticket else 0

    def get_sale_price(self, obj: Event):
        representative_ticket = obj.ticket_set.first()
        return representative_ticket.sale_price if representative_ticket else 0
