class PaymentService:
    def process_payment(self, amount):
        print(f"LOG: Processing payment of {amount}")
        if amount <= 0:
            raise ValueError("Invalid amount")
        print("Payment processed")


if __name__ == '__main__':
    service = PaymentService()
    service.process_payment(75)

    try:
        service.process_payment(0)
    except ValueError as e:
        print(f"Error: {e}")