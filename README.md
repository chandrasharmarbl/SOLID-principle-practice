# SOLID Principles in Practice

This repository demonstrates the SOLID principles of object-oriented design with practical Python examples. Each principle is illustrated with both a **messy (non-compliant) version** and a **clean (compliant) version**, along with live code examples.

---

## 📚 Table of Contents

1. [Single Responsibility Principle (SRP)](#single-responsibility-principle-srp)
2. [Open/Closed Principle (OCP)](#openclosed-principle-ocp)
3. [Liskov Substitution Principle (LSP)](#liskov-substitution-principle-lsp)
4. [Interface Segregation Principle (ISP)](#interface-segregation-principle-isp)
5. [Dependency Inversion Principle (DIP)](#dependency-inversion-principle-dip)

---

## Single Responsibility Principle (SRP)

> **A class should have one, and only one, reason to change.**

### ❌ Messy Version (Violates SRP)

```python
# payment_messy.py
class PaymentService:
    def process_payment(self, amount):
        print(f"LOG: Processing payment of {amount}")  # ← Logging responsibility mixed in
        if amount <= 0:
            raise ValueError("Invalid amount")
        print("Payment processed")
```

**Problems:**
- The `PaymentService` class has TWO responsibilities:
  1. Processing payments
  2. Logging messages
- If you need to change logging format, you must modify the payment processing logic
- Difficult to test payment logic in isolation

### ✅ Correct Version (Follows SRP)

```python
# payment.py
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
```

**Benefits:**
- `Logger` has ONE responsibility: logging
- `PaymentService` has ONE responsibility: processing payments
- Each class can be modified independently
- Easy to test payment logic separately from logging

### 🎯 Live Examples

```python
# Example usage
logger = Logger()
payment_service = PaymentService(logger)

# Process valid payment
payment_service.process_payment(100)
# Output: LOG: Processing payment of 100
#         Payment processed

# Handle invalid payment
try:
    payment_service.process_payment(-50)
except ValueError as e:
    print(f"Error: {e}")
# Output: LOG: Processing payment of -50
#         Error: Invalid amount
```

---

## Open/Closed Principle (OCP)

> **Software entities should be open for extension, closed for modification.**

### ❌ Messy Version (Violates OCP)

```python
# notification_messy.py
class NotificationService:
    def send(self, type, message):
        if type == "email":
            print(f"Email: {message}")
        elif type == "sms":
            print(f"SMS: {message}")
        # ← To add a new notification type, we MODIFY this class
```

**Problems:**
- Adding new notification types requires modifying the existing class
- Each new type requires adding a new `elif` branch
- High risk of breaking existing functionality
- Violates the Open/Closed Principle

### ✅ Correct Version (Follows OCP)

```python
# notification.py
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
```

**Benefits:**
- Open for extension: Add new notifiers by creating new classes
- Closed for modification: No need to change existing code
- Easy to add new notification types (e.g., SlackNotifier, PushNotifier)

### 🎯 Live Examples

```python
# Example: Email notification
email_notifier = EmailNotifier()
email_service = NotificationService(email_notifier)
email_service.notify("Welcome to our service!")
# Output: Email: Welcome to our service!

# Example: SMS notification
sms_notifier = SMSNotifier()
sms_service = NotificationService(sms_notifier)
sms_service.notify("Your code is 123456")
# Output: SMS: Your code is 123456

# Adding new notifier type without modifying existing code
class SlackNotifier(Notifier):
    def send(self, message):
        print(f"Slack: {message}")

slack_notifier = SlackNotifier()
slack_service = NotificationService(slack_notifier)
slack_service.notify("Deployment successful!")
# Output: Slack: Deployment successful!
```

---

## Liskov Substitution Principle (LSP)

> **Derived classes must be substitutable for their base classes.**

### ❌ Messy Version (Violates LSP)

```python
# file_processing_messy.py
class File:
    def read(self):
        pass


class ReadOnlyFile(File):
    def read(self):
        return "data"

    def write(self):
        raise Exception("Cannot write")  # ← Violates LSP!
```

**Problems:**
- `ReadOnlyFile` cannot be safely substituted for `File`
- Client code expecting a `File` may break if it calls `write()`
- The exception is a runtime surprise, not a compile-time guarantee

### ✅ Correct Version (Follows LSP)

```python
# file_processing.py
class Readable:
    def read(self):
        pass


class Writable:
    def write(self, data):
        pass


class ReadOnlyFile(Readable):
    def read(self):
        return "data"


class ReadWriteFile(Readable, Writable):
    def read(self):
        return "data"

    def write(self, data):
        print("Writing:", data)
```

**Benefits:**
- Each class implements only the methods it can support
- No unexpected exceptions
- Contracts are clear from the class definition
- `ReadOnlyFile` can be safely substituted wherever `Readable` is expected

### 🎯 Live Examples

```python
# Example: ReadOnlyFile (implements only Readable)
read_only = ReadOnlyFile()
content = read_only.read()
print(f"Read content: {content}")
# Output: Read content: data

# Example: ReadWriteFile (implements both Readable and Writable)
read_write = ReadWriteFile()
read_write.write("New data")
content = read_write.read()
print(f"Read content: {content}")
# Output: Writing: New data
#         Read content: data

# Safe substitution - ReadOnlyFile can be used anywhere Readable is expected
def process_file(readable: Readable):
    return readable.read()

result = process_file(read_only)  # ✅ Works without issues
```

---

## Interface Segregation Principle (ISP)

> **Clients should not be forced to depend on interfaces they don't use.**

### ❌ Messy Version (Violates ISP)

```python
# smart_device_messy.py
class SmartDevice:
    def turn_on(self): pass
    def play_music(self): pass


class SmartLight(SmartDevice):
    def turn_on(self):
        print("Light on")

    def play_music(self):
        raise Exception("Not supported")  # ← Forced to implement unused methods
```

**Problems:**
- `SmartLight` is forced to implement `play_music()` even though it doesn't support it
- Fat interface with methods that aren't always used
- Leads to confusing exceptions at runtime

### ✅ Correct Version (Follows ISP)

```python
# smart_device.py
class Switchable:
    def turn_on(self):
        pass


class MusicPlayer:
    def play_music(self):
        pass


class SmartLight(Switchable):
    def turn_on(self):
        print("Light on")


class SmartSpeaker(Switchable, MusicPlayer):
    def turn_on(self):
        print("Speaker on")

    def play_music(self):
        print("Playing music")
```

**Benefits:**
- Each class implements only the interfaces it needs
- No forced dependencies on unused methods
- Clear contracts about what each device can do
- Easy to compose functionality with multiple inheritance

### 🎯 Live Examples

```python
# Example: SmartLight only supports Switchable interface
light = SmartLight()
light.turn_on()
# Output: Light on

# Example: SmartSpeaker supports both Switchable and MusicPlayer
speaker = SmartSpeaker()
speaker.turn_on()
speaker.play_music()
# Output: Speaker on
#         Playing music

# Type-safe usage - devices can be used based on their actual capabilities
def operate_device(switchable: Switchable):
    switchable.turn_on()

operate_device(light)     # ✅ Works perfectly
operate_device(speaker)   # ✅ Also works - SmartSpeaker is Switchable
```

---

## Dependency Inversion Principle (DIP)

> **High-level modules should not depend on low-level modules. Both should depend on abstractions.**

### ❌ Messy Version (Violates DIP)

```python
# payment_gateway_messy.py
class Stripe:
    def pay(self, amount):
        print("Paid via Stripe")


class Checkout:
    def __init__(self):
        self.gateway = Stripe()  # ← Directly depends on Stripe implementation

    def complete(self, amount):
        self.gateway.pay(amount)
```

**Problems:**
- `Checkout` depends directly on the concrete `Stripe` class
- Cannot easily switch to different payment gateways
- Hard to test with mock payment gateways
- High coupling between classes

### ✅ Correct Version (Follows DIP)

```python
# payment_gateway.py
from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class Stripe(PaymentGateway):
    def pay(self, amount):
        print("Paid via Stripe")


class Razorpay(PaymentGateway):
    def pay(self, amount):
        print("Paid via Razorpay")


class Checkout:
    def __init__(self, gateway: PaymentGateway):
        self.gateway = gateway  # ← Depends on abstraction, not concrete class

    def complete(self, amount):
        self.gateway.pay(amount)
```

**Benefits:**
- `Checkout` depends on the abstract `PaymentGateway`
- Easy to switch between different payment providers
- Simple to test with mock implementations
- Loose coupling between components

### 🎯 Live Examples

```python
# Example: Using Stripe
stripe = Stripe()
checkout1 = Checkout(stripe)
checkout1.complete(100)
# Output: Paid via Stripe

# Example: Using Razorpay (no changes to Checkout needed!)
razorpay = Razorpay()
checkout2 = Checkout(razorpay)
checkout2.complete(200)
# Output: Paid via Razorpay

# Easy to add new payment gateways
class PayPal(PaymentGateway):
    def pay(self, amount):
        print("Paid via PayPal")

paypal = PayPal()
checkout3 = Checkout(paypal)
checkout3.complete(150)
# Output: Paid via PayPal

# Easy to mock for testing
class MockPaymentGateway(PaymentGateway):
    def pay(self, amount):
        print(f"[TEST] Mock payment of {amount}")

mock = MockPaymentGateway()
test_checkout = Checkout(mock)
test_checkout.complete(500)
# Output: [TEST] Mock payment of 500
```

---

## 🚀 Running the Examples

Each file contains a `if __name__ == '__main__':` block with executable examples:

```bash
# Run individual examples
python single_reponsibility/payment.py
python open_closed_principle/notification.py
python lsp/file_processing.py
python isp/smart_device.py
python dip/payment_gateway.py

# Run messy versions to see the issues
python single_reponsibility/payment_messy.py
python open_closed_principle/notification_messy.py
python lsp/file_processing_messy.py
python isp/smart_device_messy.py
python dip/payment_gateway_messy.py
```

---

## 📋 Summary Comparison

| Principle | Problem | Solution |
|-----------|---------|----------|
| **SRP** | Classes have multiple responsibilities | Split into single-purpose classes |
| **OCP** | Need to modify classes for new features | Use inheritance/polymorphism for extension |
| **LSP** | Subclasses break expected behavior | Ensure proper inheritance contracts |
| **ISP** | Classes forced to implement unused methods | Segregate into smaller, focused interfaces |
| **DIP** | High coupling to concrete implementations | Depend on abstractions, not concrete classes |

---

## 💡 Key Takeaways

1. **SRP**: One class, one reason to change
2. **OCP**: Extend functionality without modifying existing code
3. **LSP**: Derived classes must be proper substitutes
4. **ISP**: Don't force classes to depend on unused methods
5. **DIP**: Depend on abstractions, not concrete implementations

Following SOLID principles leads to:
- ✅ More maintainable code
- ✅ Easier to test
- ✅ Better reusability
- ✅ Reduced coupling
- ✅ Easier to extend and modify

---

## 📖 References

- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Real Python - SOLID Principles in Python](https://realpython.com/solid-principles-python/)
- Python's `abc` module for abstract base classes
