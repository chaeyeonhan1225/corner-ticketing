from event.models import Ticket, TicketInventory


class TicketInventoryService:
    def __init__(self, ticket: Ticket):
        self.ticket = ticket

    def update(self, quantity: int):
        inventory = TicketInventory.objects.filter(ticket=self.ticket).first()
        inventory.quantity = quantity
        inventory.save()

        # TODO: history add task
        return inventory
