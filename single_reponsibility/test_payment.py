import pytest
from unittest.mock import Mock, create_autospec
from payment import PaymentService, Logger

def test_process_payment_logs_message():
    mock_logger = Mock()

    service = PaymentService(mock_logger)
    service.process_payment(100)

    mock_logger.log.assert_called_once_with("Processing payment of 100")


def test_process_payment_success_does_not_raise():
    mock_logger = Mock()

    service = PaymentService(mock_logger)

    service.process_payment(50)


def test_process_payment_invalid_amount_raises():
    mock_logger = Mock()

    service = PaymentService(mock_logger)

    with pytest.raises(ValueError, match="Invalid amount"):
        service.process_payment(-10)

    mock_logger.log.assert_called_once_with("Processing payment of -10")


def test_process_payment_with_autospec_logger():
    mock_logger = create_autospec(Logger)

    service = PaymentService(mock_logger)
    service.process_payment(200)

    mock_logger.log.assert_called_once_with("Processing payment of 200")