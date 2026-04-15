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

### 🧪 Testing SRP (test_payment.py)

The test file `test_payment.py` verifies that the SRP is properly applied:

- **`test_process_payment_logs_message()`**: Verifies that `PaymentService` correctly delegates logging to the `Logger` class. By mocking the logger, we isolate payment logic from logging concerns and ensure they're truly separated.
  
- **`test_process_payment_invalid_amount_raises()`**: Ensures the payment processing logic works independently. The mock logger confirms logging happens even when validation fails.
  
- **`test_process_payment_with_autospec_logger()`**: Uses `create_autospec` to enforce the `Logger` contract, ensuring `PaymentService` depends only on the expected interface.

**Why these tests matter**: They prove that payment processing and logging are independent responsibilities that can be modified separately without affecting each other.

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

### 🧪 Testing OCP (test_notification.py)

The test file `test_notification.py` validates that the OCP principle enables extension without modification:

- **`test_notify_calls_send_with_mock()`**: Verifies that `NotificationService` works with any `Notifier` implementation through mocking. The service doesn't care about specific implementations.
  
- **`test_notify_with_autospec_enforces_contract()`**: Uses `create_autospec` to enforce strict interface compliance. This ensures new notifiers must follow the contract.
  
- **`test_ocp_extension_new_notifier()`**: Demonstrates adding a new `PushNotifier` without modifying existing code. The test runs directly to show real extensibility.

**Why these tests matter**: They prove that new notification types can be added by creating new classes that inherit from `Notifier`, without touching `NotificationService` code.

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

### 🧪 Testing LSP (test_file_processing.py)

The test file `test_file_processing.py` ensures that derived classes are proper substitutes for their base class contracts:

- **`test_read_only_file_honours_readable_contract()` and `test_read_write_file_honours_readable_contract()`**: Verify that both `ReadOnlyFile` and `ReadWriteFile` can be used anywhere a `Readable` is expected. The mock demonstrates safe substitution.
  
- **`test_both_subtypes_return_same_type_from_read()`**: Confirms that `read()` returns the same type from both classes, preventing unexpected type violations at runtime.
  
- **`test_subtypes_are_interchangeable_in_same_consumer()`**: Proves that a consumer function works identically whether passed a `ReadOnlyFile` or `ReadWriteFile`, validating true substitutability.

**Why these tests matter**: They ensure that subclasses don't violate the parent class contract. Without LSP tests, you might discover at runtime that a subclass breaks expected behavior.

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

### 🧪 Testing ISP (test_smart_device.py)

The test file `test_smart_device.py` validates that each class implements only the interfaces it needs:

- **`test_light_only_needs_switchable()`**: Verifies that `SmartLight` only requires the `Switchable` interface, not the `MusicPlayer` interface.
  
- **`test_light_does_not_expose_play_music()` and `test_real_light_has_no_play_music()`**: Assert that `SmartLight` doesn't implement `play_music()` at all, preventing the fat interface problem.
  
- **`test_light_turn_on_called_with_mock()`**: Shows that devices can be used based on their actual capabilities through type-safe interfaces.
  
- **`test_speaker_satisfies_switchable()`**: Demonstrates that `SmartSpeaker` can be used wherever `Switchable` is expected, even though it implements additional interfaces.

**Why these tests matter**: They catch the ISP violation problem early. If you accidentally force a class to implement unused methods, these tests will fail with clear assertions.

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

### 🎯 Live Examples with pytest-mock

```python
# test_payment_gateway.py
import pytest
from unittest.mock import call
from payment_gateway import Checkout, Stripe, Razorpay, PaymentGateway


class TestCheckoutWithMock:
    """Test Checkout with mocked PaymentGateway (DIP in action)"""
    
    def test_checkout_calls_gateway_pay_method(self, mocker):
        """Verify that Checkout delegates to the gateway abstraction"""
        # Create a mock PaymentGateway
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)
        
        # Checkout works with ANY gateway implementation
        checkout = Checkout(mock_gateway)
        
        # Execute checkout
        checkout.complete(100)
        
        # Verify the abstraction was called correctly
        mock_gateway.pay.assert_called_once_with(100)

    def test_checkout_with_different_gateways(self, mocker):
        """Test that Checkout is independent of specific gateway implementations"""
        # Mock different gateway implementations
        mock_stripe = mocker.MagicMock(spec=PaymentGateway)
        mock_razorpay = mocker.MagicMock(spec=PaymentGateway)
        
        # Same Checkout code works with any gateway
        checkout_stripe = Checkout(mock_stripe)
        checkout_razorpay = Checkout(mock_razorpay)
        
        checkout_stripe.complete(100)
        checkout_razorpay.complete(200)
        
        # Each gateway was called appropriately
        mock_stripe.pay.assert_called_once_with(100)
        mock_razorpay.pay.assert_called_once_with(200)

    def test_checkout_isolates_gateway_failures(self, mocker):
        """Test failure scenarios without real gateway dependencies"""
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)
        
        # Simulate payment failure
        mock_gateway.pay.side_effect = Exception("Payment failed")
        
        checkout = Checkout(mock_gateway)
        
        # Verify failure is handled correctly
        with pytest.raises(Exception, match="Payment failed"):
            checkout.complete(100)


# Run tests: pytest test_payment_gateway.py -v
```

**Benefits of mocking for DIP:**
- ✅ Test `Checkout` without depending on real payment gateways
- ✅ Verify the abstraction contract is followed correctly
- ✅ Isolate failures and edge cases easily
- ✅ No need for test databases or external APIs
- ✅ Fast, reliable tests that prove DIP is working

### 🧪 Testing DIP (test_payment_gateway.py)

The test file `test_payment_gateway.py` demonstrates why DIP is essential for testability:

- **`test_checkout_calls_gateway_pay_method()`**: Uses `mocker.MagicMock` with `spec=PaymentGateway` to verify that `Checkout` correctly delegates to the abstraction. If `Checkout` depended on concrete `Stripe`, this test would be impossible without heavy setup.\n  
- **`test_checkout_with_different_gateways()`**: Proves the core benefit of DIP: the same `Checkout` code works with multiple gateway implementations. Each can be tested independently with mocks.\n  
- **`test_checkout_isolates_gateway_failures()`**: Simulates payment failures using `side_effect` without touching real payment systems. This tests error handling in isolation.\n\n**Why these tests matter**: By depending on the `PaymentGateway` abstraction, `Checkout` becomes testable without external dependencies. This is impossible if it directly instantiates `Stripe()`. DIP enables fast, reliable unit tests.\n\n---

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
