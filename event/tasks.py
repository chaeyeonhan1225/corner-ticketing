from celery import shared_task
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from common.utils import GmailEmailSender
from event.models import UserTicket

User = get_user_model()


@shared_task
def send_transfer_request_email(giver_id, receiver_id, origin_ticket_id, transfer_code):
    giver = User.objects.get(id=giver_id)
    receiver = User.objects.get(id=receiver_id)
    origin_ticket = UserTicket.objects.filter(uuid=origin_ticket_id).select_related("ticket", "ticket__event").first()

    context = {
        "giver_nickname": giver.nickname,
        "receiver_nickname": receiver.nickname,
        "transfer_code": transfer_code,
        "ticket_event_title": origin_ticket.ticket.event.title,
        "ticket_started_at": origin_ticket.ticket.started_at.strftime("%Y-%m-%d %H:%M"),
        "ticket_ended_at": origin_ticket.ticket.ended_at.strftime("%Y-%m-%d %H:%M"),
    }

    title = f"{giver.nickname}님이 티켓을 선물하였어요."
    content = render_to_string("email_templates/ticket_transfer.html", context)

    GmailEmailSender(
        sender="gkscodus11@gmail.com", receiver=receiver.email, title=title, content=content, subtype="html"
    ).send_email()
