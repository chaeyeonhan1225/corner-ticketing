from celery import shared_task
from django.contrib.auth import get_user_model

from common.utils import GmailEmailSender

User = get_user_model()


@shared_task
def send_joined_email(user_id: int):
    user = User.objects.get(id=user_id)
    content = """
                <html>
                  <head></head>
                  <body>
                    <h2>회원가입을 축하드립니다!</h2>
                    <p>{user_nickname}님의 회원가입을 진십으로 축하드립니다.</p>
                    <p>(이 메일은 테스트용입니다.)</p>
                  </body>
                </html>
                """.format(
        user_nickname=user.nickname
    )

    GmailEmailSender(
        sender="gkscodus11@gmail.com",
        receiver="gkscodus11@naver.com",
        title="회원 가입을 축하드립니다!",
        content=content,
        subtype="html",
    ).send_email()
