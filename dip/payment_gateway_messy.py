class Stripe:
    def pay(self, amount):
        print("Paid via Stripe")


class Checkout:
    def __init__(self):
        self.gateway = Stripe()

    def complete(self, amount):
        self.gateway.pay(amount)


if __name__ == '__main__':
    checkout = Checkout()
    checkout.complete(150)