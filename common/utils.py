import smtplib

from abc import ABCMeta, abstractmethod
from email.message import EmailMessage

from django.conf import settings


class EmailSender(metaclass=ABCMeta):
    @abstractmethod
    def send_email(self):
        pass


class GmailEmailSender(EmailSender):
    def __init__(self, sender, receiver, title, content, subtype):
        self.sender = sender if not settings.DEBUG else settings.TEST_SENDER_EMAIL
        self.receiver = receiver if not settings.DEBUG else settings.TEST_RECEIVER_EMAIL
        self.title = title
        self.content = content
        self.subtype = subtype
        self.message = EmailMessage()

    def __set_message(self):
        self.message['Subject'] = self.title
        self.message['From'] = self.sender
        self.message['To'] = self.receiver
        self.message.add_alternative(self.content, subtype=self.subtype)

    def send_email(self):
        self.__set_message()
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(self.sender, settings.GMAIL_APP_PASSWORD)
            s.sendmail(self.sender, self.receiver, self.message.as_string())





