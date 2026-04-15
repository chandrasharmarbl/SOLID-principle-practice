from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class Stripe(PaymentGateway):
    def pay(self, amount):
        print("Paid via Stripe: ${:.2f}".format(amount))


class Razorpay(PaymentGateway):
    def pay(self, amount):
        print("Paid via Razorpay: ${:.2f}".format(amount))


class Checkout:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway

    def complete(self, amount):
        self.gateway.pay(amount)


if __name__ == '__main__':
    stripe = Stripe()
    checkout1 = Checkout(stripe)
    checkout1.complete(100)

    razorpay = Razorpay()
    checkout2 = Checkout(razorpay)
    checkout2.complete(200)