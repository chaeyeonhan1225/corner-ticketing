from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from event.services.ticket_purchase_service import TicketPurchaseService


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
