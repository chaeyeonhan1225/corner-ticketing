import time
from django.db import transaction
from django.core.cache import cache

from ticket.models import Ticket, UserTicket
from ticket.exceptions import NotEnoughTicketsException


class TicketPurchaseService:
    def __init__(self, user):
        self.user = user

    def update_inventory_with_cache_lock_max_try(self, ticket: Ticket, purchase_quantity: int):
        user_tickets = []

        max_try = 3
        ticket_key = f'ticket_purchase_lock_{ticket.id}'
        while max_try > 0:
            max_try -= 1
            print(f'max_try = {max_try}')
            if cache.set(ticket_key, 'True', nx=True):
                try:
                    user_tickets = self.update_inventory(ticket, purchase_quantity)
                    break
                except NotEnoughTicketsException as e:
                    print('Not enough tickets')
                    raise e
                finally:
                    cache.delete(ticket_key)
            else:
                print('재시도!')
                time.sleep(0.5)

        if max_try == 0:
            raise Exception('max try 횟수를 초과했습니다.')
        print(f'user_tickets = {user_tickets}')
        return user_tickets

    def update_inventory_with_cache_lock(self, ticket: Ticket, purchase_quantity: int):
        user_tickets = []
        ticket_key = f'ticket_purchase_lock_{ticket.id}'
        while True:
            if cache.set(ticket_key, 'True', nx=True):
                try:
                    user_tickets = self.update_inventory(ticket, purchase_quantity)
                except NotEnoughTicketsException as e:
                    print('Not Enough Tickets')
                    raise e
                finally:
                    cache.delete(ticket_key)
                    break
            else:
                print('재시도!')
                time.sleep(0.5)
        return user_tickets
        
    def update_inventory(self, ticket: Ticket, purchase_quantity: int):
        inventory = ticket.ticketinventory_set.first()
        print(f'Purchase Inventory = {inventory.quantity}')
        print(f'Inventory = {inventory.quantity - purchase_quantity}')
        if inventory and inventory.quantity >= purchase_quantity:
            inventory.quantity -= purchase_quantity
            user_tickets = [UserTicket(ticket=ticket, owner=self.user) for i in range(0, purchase_quantity)]
            UserTicket.objects.bulk_create(user_tickets)
        else:
            raise NotEnoughTicketsException('남은 티켓이 없습니다.')

        inventory.save()
        return user_tickets

    @transaction.atomic
    def purchase_ticket(self, ticket_id: int, ticket_quantity: int):
        try:
            print(f'Purchase Ticket {ticket_id} with quantity {ticket_quantity}')
            ticket = Ticket.objects.get(id=ticket_id)
            user_tickets = self.update_inventory_with_cache_lock_max_try(ticket, ticket_quantity)
            return user_tickets
        except NotEnoughTicketsException as ne:
            print('NotEnoughTicketsException', ne)
            raise ne
        except Exception as e:
            import traceback
            print(e)
            traceback.print_tb(e.__traceback__)
