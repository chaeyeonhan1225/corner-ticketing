from datetime import datetime
from django.conf import settings
from django.test import TestCase
from django.contrib.auth import get_user_model

from corner_ticketing.celery import app

from event.models import Ticket, EventType, TicketInventory, UserTicket, Event
from event.services.ticket_service import TicketService
from event.services.ticket_purchase_service import TicketPurchaseService
from event.services.ticket_transfer_service import TicketTransferService


# Create your tests here.
class TicketTest(TestCase):
    def setUp(self):
        settings.DEBUG = True   # Test 환경에서는 DEBUG=False가 default, 메일이 잘못 나가는 것을 방지
        app.conf.update(CELERY_ALWAYS_EAGER=True)
    @classmethod
    def setUpTestData(cls):
        event = Event.objects.create(
            title='[잠실]7.16 엘지 vs 롯데',
            subtitle='엘롯라시코 1차전',
            type=EventType.SPORTS
        )
        cls.event = event
        param = {
            'event_id': event.id,
            'started_at': datetime.now(),
            'regular_price': 10000,
            'ended_price': 10000,
            'ended_at': datetime.now(),
            'quantity': 10
        }
        cls.ticket = TicketService().create(param)
        User = get_user_model()
        cls.userA = User.objects.create_user(
            email="tester1@gmail.com",
            password="test123456",
            nickname="tester1"
        )
        cls.userB = User.objects.create_user(
            email="tester2@gmail.com",
            password="test123456",
            nickname="tester2"
        )


    def test_ticket_transfer(self):
        userA_tickets = TicketPurchaseService(self.userA).purchase_ticket(
            ticket_id=self.ticket.id,
            ticket_quantity=1
        )

        userA_ticket = userA_tickets[0] if userA_tickets else None
        result = TicketTransferService().request_transfer(
            giver=self.userA,
            receiver=self.userB,
            origin_ticket=userA_ticket
        )
        print(result)

        TicketTransferService().receive_ticket(
            code=result,
            receiver=self.userB
        )










