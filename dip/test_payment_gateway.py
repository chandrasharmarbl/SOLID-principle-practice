import pytest
from unittest.mock import call
from payment_gateway import Checkout, Stripe, Razorpay, PaymentGateway


class TestCheckoutWithMock:

    def test_checkout_calls_gateway_pay_method(self, mocker):
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)

        checkout = Checkout(mock_gateway)

        checkout.complete(100)

        mock_gateway.pay.assert_called_once_with(100)

    def test_checkout_calls_gateway_multiple_times(self, mocker):
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)
        checkout = Checkout(mock_gateway)

        checkout.complete(100)
        checkout.complete(200)
        checkout.complete(50)

        assert mock_gateway.pay.call_count == 3
        mock_gateway.pay.assert_has_calls([
            call(100),
            call(200),
            call(50),
        ])

    def test_checkout_with_different_payment_amounts(self, mocker):
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)
        checkout = Checkout(mock_gateway)

        amounts = [10.50, 99.99, 1000.00]

        for amount in amounts:
            checkout.complete(amount)

        for i, amount in enumerate(amounts):
            assert mock_gateway.pay.call_args_list[i] == call(amount)

    def test_checkout_isolates_gateway_failures(self, mocker):
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)

        mock_gateway.pay.side_effect = Exception("Payment failed")

        checkout = Checkout(mock_gateway)

        with pytest.raises(Exception, match="Payment failed"):
            checkout.complete(100)

    def test_checkout_with_return_value_mock(self, mocker):
        mock_gateway = mocker.MagicMock(spec=PaymentGateway)
        mock_gateway.pay.return_value = "txn_12345"

        checkout = Checkout(mock_gateway)
        checkout.complete(100)

        mock_gateway.pay.assert_called_once_with(100)

    def test_checkout_gateway_independence(self, mocker):
        mock_gateway_1 = mocker.MagicMock(spec=PaymentGateway)
        mock_gateway_2 = mocker.MagicMock(spec=PaymentGateway)

        checkout1 = Checkout(mock_gateway_1)
        checkout2 = Checkout(mock_gateway_2)

        checkout1.complete(100)
        checkout2.complete(200)

        mock_gateway_1.pay.assert_called_once_with(100)
        mock_gateway_2.pay.assert_called_once_with(200)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
