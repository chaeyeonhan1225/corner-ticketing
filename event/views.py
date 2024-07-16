from django.core.cache import cache
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import status, serializers
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from enumfields.drf.serializers import EnumSerializerField, EnumSupportSerializerMixin
from event.models import Event, Ticket, TicketInventory
from event.services.ticket_purchase_service import TicketPurchaseService
from event.services.ticket_inventory_service import TicketInventoryService


class EventSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,) # TODO: create는 AdminOnly로 변경


# class TicketFilterSet(FilterSet):
#     title = CharFilter(field_name='title', lookup_expr='contains')

class TicketSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class TicketView(ListAPIView):
    permission_classes = (AllowAny, )
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filterset_class = TicketFilterSet


class TicketReserveView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request, ticket_id):
        try:
            key = f'ticket_waiting_{ticket_id}'
            waiting = cache.get(key)
            if waiting is None:
                cache.set(key, 0)

            result = cache.incr(key)
            print(result)
            return Response(data={'waiting': result})
        except Exception as e:
            print(e)
            return Response(data={'message': f'{e}'})


class TicketPurchaseView(APIView):
    def post(self, request, ticket_id):
        try:
            result = TicketPurchaseService(request.user).purchase_ticket(
                ticket_id=ticket_id,
                ticket_quantity=int(request.data["quantity"])
            )
            print(f'result = {result}')
            return Response(data={"message": "success"})
        except APIException as ae:
            return Response(data={"detail": ae.detail}, status=ae.status_code)
        except Exception as e:
            import traceback
            traceback.print_tb(e.__traceback__)
            return Response(data={"message": "fail"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TicketInventorySerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = TicketInventory
        fields = '__all__'

class TicketInventoryView(APIView):
    def get(self, request, ticket_id):
        inventory = TicketInventory.objects.filter(ticket_id=ticket_id).first()
        if inventory is None:
            raise Exception()

        serializer = TicketInventorySerializer(inventory)
        return Response(data=serializer.data)


# TODO: quantity 값은 실시간으로 바뀌는데 어떻게 할 지 고민중.. 그냥 increase, decrease만 해야하나?
# TODO: 변경하는 동안 quantity 값에 Lock을 걸자!
class TicketInventoryUpdateView(APIView):
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            quantity = int(request.data.get('quantity'))
            inventory = TicketInventoryService(ticket).update(quantity)
            return Response(data=TicketInventorySerializer(inventory).data)
        except Ticket.DoesNotExist:
            return Response(data={'detail': 'Ticket does not Exist'}, status=status.HTTP_404_NOT_FOUND)


class TicketTransferView(APIView):
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)

        except Ticket.DoesNotExist:
            return Response(data={"detail": "존재하지 않는 티켓입니다."}, status=status.HTTP_404_NOT_FOUND)