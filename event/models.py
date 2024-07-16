import uuid

from django.db import models
from enum import unique
from enumfields import Enum, EnumField

from common.models import TimeRecordingMixin


@unique
class EventType(Enum):
    CONCERT = "CONCERT"  # 공연
    SPORTS = "SPORTS"  # 스포츠
    ETC = "ETC" # 기타


@unique
class TicketState(Enum):
    READY = "READY"  # 판매대기
    SALE = "SALE"  # 판매중
    SOLD_OUT = "SOLD_OUT"  # 품절
    PAUSED = "PAUSED"  # 판매 일시 중지
    CLOSED = "CLOSED"  # 판매 종료

@unique
class UserTicketState(Enum):
    NOT_USED = "NOT_USED"  # 미사용
    USED = "USED"  # 사용 완료
    NO_SHOW = "NO_SHOW"  # 노쇼
    CANCELED = "CANCELED"  # 취소
    TRANSFERRED = "TRANSFERRED"  # 선물함


class Event(TimeRecordingMixin):
    title = models.CharField(max_length=40, verbose_name='이벤트 타이틀')
    subtitle = models.CharField(max_length=80, verbose_name='이벤트 서브타이틀')
    type = EnumField(EventType, max_length=20, verbose_name='이벤트 타입', default=EventType.CONCERT)

    class Meta:
        db_table = 'event'
        verbose_name = '이벤트'


"""
티켓은 항상 한 번만 사용할 수 있는걸로 정의한다.(여러번 사용가능 티켓은 존재하지 않음)
자리도 없다고 가정
"""


class Ticket(TimeRecordingMixin):
    event = models.ForeignKey('event.Event', on_delete=models.CASCADE, verbose_name='공연/경기 ID')
    started_at = models.DateTimeField(null=True, blank=True, verbose_name='공연/경기 입장시간')
    ended_at = models.DateTimeField(null=True, blank=True, verbose_name='공연/경기 퇴장시간')
    status = EnumField(TicketState, max_length=20, verbose_name='티켓 상태', default=TicketState.READY)

    class Meta:
        db_table = 'ticket'
        verbose_name = '티켓'

class TicketInventory(TimeRecordingMixin):
    ticket = models.ForeignKey('event.Ticket', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, verbose_name='수량')

    class Meta:
        db_table = 'ticket_inventory'
        verbose_name = '티켓 재고'

class TicketInventoryHistory(TimeRecordingMixin):
    inventory = models.ForeignKey('event.TicketInventory', on_delete=models.CASCADE)
    before = models.JSONField(null=True, blank=True, verbose_name='수정 전')
    after = models.JSONField(null=True, blank=False, verbose_name='수정 후')

    def __str__(self):
        return f'{self.inventory.id}_history_{self.id}'

    class Meta:
        db_table = 'ticket_inventory_history'
        verbose_name = '티켓 재고 변경 이력'


class UserTicket(TimeRecordingMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey('event.Ticket', on_delete=models.CASCADE, null=False, blank=False)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, null=False, blank=False,
                             verbose_name='티켓 소유 유저', related_name='owner')
    giver = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name='선물 해준 유저', related_name='giver')
    status = EnumField(UserTicketState, max_length=20, verbose_name='티켓 상태', default=UserTicketState.NOT_USED)
    used_at = models.DateTimeField(null=True, verbose_name='사용 시간')
    canceled_at = models.DateTimeField(null=True, verbose_name='취소 시간')
    transferred_at = models.DateTimeField(null=True, verbose_name='선물 시간')

    def __str__(self):
        if self.giver:
            return f'{self.owner}_{self.ticket}({self.giver})'
        return f'{self.owner}_{self.ticket}'

    class Meta:
        db_table = 'user_ticket'
        verbose_name = '유저가 구매한 티켓'


class UserTicketHistory(TimeRecordingMixin):
    user_ticket = models.ForeignKey('event.UserTicket', on_delete=models.CASCADE, null=False, blank=False, verbose_name='유저 티켓')
    before = models.JSONField(null=True, blank=True, verbose_name='수정 전')
    after = models.JSONField(null=True, blank=False, verbose_name='수정 후')

    def __str__(self):
        return f'{self.user_ticket.id}_history_{self.id}'

    class Meta:
        db_table = 'user_ticket_history'
        verbose_name = '유저가 구매한 티켓 변경 이력'

