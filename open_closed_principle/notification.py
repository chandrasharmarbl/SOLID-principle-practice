from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, message):
        pass


class EmailNotifier(Notifier):
    def send(self, message):
        print(f"Email: {message}")


class SMSNotifier(Notifier):
    def send(self, message):
        print(f"SMS: {message}")


class NotificationService:
    def __init__(self, notifier: Notifier):
        self.notifier = notifier

    def notify(self, message):
        self.notifier.send(message)


if __name__ == '__main__':
    email_notifier = EmailNotifier()
    email_service = NotificationService(email_notifier)
    email_service.notify("Welcome to our service!")

    sms_notifier = SMSNotifier()
    sms_service = NotificationService(sms_notifier)
    sms_service.notify("Your code is 123456")