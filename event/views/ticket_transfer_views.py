from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from event.models import Ticket


class TicketTransferView(APIView):
    def post(self, request, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)

        except Ticket.DoesNotExist:
            return Response(data={"detail": "존재하지 않는 티켓입니다."}, status=status.HTTP_404_NOT_FOUND)