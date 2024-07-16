from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from event.models import Event


class EventSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    regular_price = serializers.SerializerMethodField()
    sale_price = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_regular_price(self, obj: Event):
        representative_ticket = obj.ticket_set.first()
        return representative_ticket.regular_price if representative_ticket else 0

    def get_sale_price(self, obj: Event):
        representative_ticket = obj.ticket_set.first()
        return representative_ticket.sale_price if representative_ticket else 0


class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all().prefetch_related('ticket_set')
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,) # TODO: permission 분리 필요


class EventDetailView(RetrieveAPIView):
    serializer_class = EventSerializer
    permission_classes = (AllowAny,)
    queryset = Event.objects.all().prefetch_related('ticket_set')