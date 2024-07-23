import time

from django.core.cache import cache
from django.db import transaction

from event.exceptions import NotEnoughTicketsException
from event.models import Ticket, UserTicket


class TicketPurchaseService:
    def __init__(self, user):
        self.user = user

    def update_inventory_with_cache_lock_max_try(self, ticket: Ticket, purchase_quantity: int):
        user_tickets = []

        max_try = 3
        ticket_key = f"ticket_purchase_lock_{ticket.id}"
        while max_try > 0:
            max_try -= 1
            print(f"max_try = {max_try}")
            if cache.set(ticket_key, "True", nx=True):
                try:
                    user_tickets = self.update_inventory(ticket, purchase_quantity)
                    break
                except NotEnoughTicketsException as e:
                    print("Not enough tickets")
                    raise e
                finally:
                    cache.delete(ticket_key)
            else:
                print("재시도!")
                time.sleep(0.5)

        if max_try == 0:
            raise Exception("max try 횟수를 초과했습니다.")

        return user_tickets

    def update_inventory_with_cache_lock(self, ticket: Ticket, purchase_quantity: int):
        user_tickets = []
        ticket_key = f"ticket_purchase_lock_{ticket.id}"
        while True:
            if cache.set(ticket_key, "True", nx=True):
                try:
                    user_tickets = self.update_inventory(ticket, purchase_quantity)
                except NotEnoughTicketsException as ne:
                    print("Not Enough Tickets")
                    raise ne
                finally:
                    cache.delete(ticket_key)
                    break
            else:
                time.sleep(0.5)
        return user_tickets

    def update_inventory(self, ticket: Ticket, purchase_quantity: int):
        inventory = ticket.ticketinventory_set.first()

        if inventory and inventory.quantity >= purchase_quantity:
            inventory.quantity -= purchase_quantity
            user_tickets = [UserTicket(ticket=ticket, owner=self.user) for i in range(0, purchase_quantity)]
            UserTicket.objects.bulk_create(user_tickets)
        else:
            raise NotEnoughTicketsException("남은 티켓이 없습니다.")

        inventory.save()
        return user_tickets

    @transaction.atomic
    def purchase_ticket(self, id: int, quantity: int):
        try:
            print(f"Purchase Ticket {id} with quantity {quantity}")
            ticket = Ticket.objects.get(id=id)
            user_tickets = self.update_inventory_with_cache_lock_max_try(ticket, quantity)
            return user_tickets
        except NotEnoughTicketsException as ne:
            print("NotEnoughTicketsException", ne)
            raise ne
        except Exception as e:
            import traceback

            print(e)
            traceback.print_tb(e.__traceback__)
