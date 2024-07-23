from django.db import transaction
from rest_framework.exceptions import ValidationError

from event.models import Event, EventType, Ticket, TicketInventory


class TicketService:
    @transaction.atomic
    def create(self, param):
        try:
            event = Event.objects.get(id=param.get("event_id"))

            ticket = Ticket(
                event=event,
                regular_price=param.get("regular_price"),
                sale_price=param.get("sale_price"),
                started_at=param.get("started_at"),
                ended_at=param.get("ended_at"),
            )
            inventory = TicketInventory(ticket=ticket, quantity=param.get("quantity"))
            ticket.save()
            inventory.save()
            return ticket
        except Event.DoesNotExist:
            raise ValidationError("")
