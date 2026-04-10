class Logger:
    def log(self, message):
        print(f"LOG: {message}")


class PaymentService:
    def __init__(self, logger: Logger):
        self.logger = logger

    def process_payment(self, amount):
        self.logger.log(f"Processing payment of {amount}")
        if amount <= 0:
            raise ValueError("Invalid amount")
        print("Payment processed")


if __name__ == '__main__':
    logger = Logger()
    payment_service = PaymentService(logger)
    payment_service.process_payment(100)

    try:
        payment_service.process_payment(-50)
    except ValueError as e:
        print(f"Error: {e}")