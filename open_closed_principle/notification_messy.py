class NotificationService:
    def send(self, type, message):
        if type == "email":
            print(f"Email: {message}")
        elif type == "sms":
            print(f"SMS: {message}")


if __name__ == '__main__':
    service = NotificationService()
    service.send("email", "Hello via email!")

    service.send("sms", "Hello via SMS!")