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
        print(settings.DEBUG)
        self.sender = sender if not settings.DEBUG else 'gkscodus11@gmail.com'
        self.receiver = receiver if not settings.DEBUG else 'gkscodus11@naver.com'
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
            s.login(self.sender, 'dhzktwhhiwhdkcnw')
            s.sendmail(self.sender, self.receiver, self.message.as_string())





