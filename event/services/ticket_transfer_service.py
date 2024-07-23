import datetime
from datetime import timezone
from typing import Any

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction

from event.models import Ticket, UserTicket, UserTicketState
from event.tasks import send_transfer_request_email
from event.utils import generate_random_slug_code

User = get_user_model()

"""
티켓 선물하기
1. 티켓을 선물하면 코드가 발급된다.   --> 코드가 꼭 필요한가? 그냥 선물해주면 안되는건가?
2. 그 코드를 입력하면 티켓을 선물 받을 수 있다.
3. 선물 받은 티켓은 다시 선물할 수 없다.
4. 누구에게 선물을 줬는지, 누구에게 받았는지 기록이 남아야 한다.
5. 상대가 선물을 받기 전에 취소할 수 있다.
"""


class TicketTransferService:
    # def __init__(self, ticket: Ticket):
    #     self.ticket = ticket

    def request_transfer(self, giver: User, receiver: User, origin_ticket: UserTicket) -> bool:
        if origin_ticket.giver is not None:
            raise Exception()

        transfer_code = generate_random_slug_code()
        cache_key = f"ticket_transfer_{transfer_code}"
        if cache.set(f"ticket_transfer_{origin_ticket.uuid}", transfer_code, nx=True, timeout=5 * 60) and cache.set(
            cache_key,
            {
                "transfer_code": transfer_code,
                "origin_ticket_id": origin_ticket.uuid,
                "giver": giver.id,
                "receiver": receiver.id,
            },
            nx=True,
            timeout=5 * 60,
        ):

            send_transfer_request_email.delay(
                giver_id=giver.id,
                receiver_id=receiver.id,
                origin_ticket_id=origin_ticket.uuid,
                transfer_code=transfer_code,
            )
            return transfer_code
        else:
            raise Exception()

    def __validate_transfer_info(self, code: str, receiver: User, transfer_info: dict[str, Any]) -> bool:
        if transfer_info is None:
            raise Exception()
        transfer_code = transfer_info.get("transfer_code")
        giver_id = transfer_info.get("giver")
        receiver_id = transfer_info.get("receiver")

        if receiver.id != receiver_id:
            raise Exception()

        if not User.objects.filter(id=giver_id).exists():
            raise Exception()

        if code != transfer_code:
            raise Exception()

    def __get_validated_origin_ticket_by_transfer_code(self, code: str, receiver: User):
        transfer_info = cache.get(f"ticket_transfer_{code}")
        self.__validate_transfer_info(code, receiver, transfer_info)

        origin_ticket = UserTicket.objects.get(uuid=transfer_info.get("origin_ticket_id"))
        return origin_ticket

    def receive_ticket(self, code: str, receiver: User):
        origin_ticket = self.__get_validated_origin_ticket_by_transfer_code(code, receiver)

        with transaction.atomic():
            origin_ticket.status = UserTicketState.TRANSFERRED
            origin_ticket.transferred_at = datetime.datetime.now()
            new_ticket = UserTicket(owner=receiver, ticket=origin_ticket.ticket, giver=origin_ticket.owner)
            origin_ticket.save()
            new_ticket.save()
            cache.delete(f"ticket_transfer_{origin_ticket.uuid}")
            cache.delete(f"ticket_transfer_{code}")

            # TODO: commit 완료시, history add
