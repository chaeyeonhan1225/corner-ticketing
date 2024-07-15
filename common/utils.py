import smtplib

from abc import ABCMeta, abstractmethod
from email.message import EmailMessage


class EmailSender(metaclass=ABCMeta):
    @abstractmethod
    def send_email(self):
        pass


class GmailEmailSender(EmailSender):
    def __init__(self, sender, receiver, title, content, subtype):
        self.sender = sender
        self.receiver = receiver
        self.title = title
        self.content = content
        self.subtype = subtype
        self.message = EmailMessage()

    def __set_message(self):
        self.message['Subject'] = self.title
        self.message['From'] = self.sender
        self.message.add_alternative(self.content, subtype=self.subtype)

    def send_email(self):
        self.__set_message()
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.starttls()
            s.login(self.sender, 'dhzktwhhiwhdkcnw')
            s.sendmail(self.sender, self.receiver, self.message.as_string())





