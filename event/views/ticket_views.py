from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from enumfields.drf.serializers import EnumSupportSerializerMixin
from prompt_toolkit.validation import ValidationError
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Event, Ticket
from event.services.ticket_service import TicketService

# class TicketFilterSet(FilterSet):
#     title = CharFilter(field_name='title', lookup_expr='contains')


class TicketSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"


class TicketCreateParamSerializer(serializers.Serializer):
    regular_price = serializers.IntegerField(help_text="티켓 정가", required=True, min_value=0)
    sale_price = serializers.IntegerField(help_text="티켓 판매가", required=True, min_value=0)
    started_at = serializers.DateTimeField(help_text="공연/전시 시작시간", required=True)
    ended_at = serializers.DateTimeField(help_text="공연/전시 종료시간", required=True)
    quantity = serializers.IntegerField(help_text="티켓 수량", required=True, min_value=1)


class TicketListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, event_id: int):
        event = Event.objects.filter(id=event_id).prefetch_related("ticket_set").first()
        serializer = TicketSerializer(event.ticket_set, many=True)
        return Response(data=serializer.data)

    def post(self, request, event_id: int):
        serializer = TicketCreateParamSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            param = {"event_id": event_id, **serializer.validated_data}
            print(f"param = {param}")
            ticket = TicketService().create(param)
            return Response(data=TicketSerializer(ticket).data)
        except ValidationError as e:
            print(e)


class TicketReserveView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, ticket_id):
        try:
            key = f"ticket_waiting_{ticket_id}"
            waiting = cache.get(key)
            if waiting is None:
                cache.set(key, 0)

            result = cache.incr(key)
            print(result)
            return Response(data={"waiting": result})
        except Exception as e:
            print(e)
            return Response(data={"message": f"{e}"})
