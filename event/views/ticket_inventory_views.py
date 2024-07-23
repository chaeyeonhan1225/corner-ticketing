from enumfields.drf.serializers import EnumSupportSerializerMixin
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from event.models import Ticket, TicketInventory
from event.services.ticket_inventory_service import TicketInventoryService


class TicketInventorySerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = TicketInventory
        fields = "__all__"


# class TicketInventoryListView(ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = TicketInventorySerializer
#
#     def get_queryset(self):
#         return TicketInventory.objects.filter(tiket_id=self.kwargs['ticket_id'])
#     def get(self, request, ticket_id):
#         inventory = TicketInventory.objects.filter(ticket_id=ticket_id).first()
#         if inventory is None:
#             raise Exception()
#
#         serializer = TicketInventorySerializer(inventory)
#         return Response(data=serializer.data)


# TODO: quantity 값은 실시간으로 바뀌는데 어떻게 할 지 고민중.. 그냥 increase, decrease만 해야하나?
# TODO: 변경하는 동안 quantity 값에 Lock을 걸자!
class TicketInventoryUpdateView(APIView):
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            quantity = int(request.data.get("quantity"))
            inventory = TicketInventoryService(ticket).update(quantity)
            return Response(data=TicketInventorySerializer(inventory).data)
        except Ticket.DoesNotExist:
            return Response(data={"detail": "Ticket does not Exist"}, status=status.HTTP_404_NOT_FOUND)
