import pytest
from abc import ABC, abstractmethod
from unittest.mock import Mock, create_autospec
from notification import Notifier, EmailNotifier, SMSNotifier, NotificationService

def test_notify_calls_send_with_mock():
    mock_notifier = Mock()

    service = NotificationService(mock_notifier)
    service.notify("Hello")

    mock_notifier.send.assert_called_once_with("Hello")


def test_notify_with_autospec_enforces_contract():
    mock_notifier = create_autospec(Notifier)

    service = NotificationService(mock_notifier)
    service.notify("Strict Test")

    mock_notifier.send.assert_called_once_with("Strict Test")


def test_ocp_extension_new_notifier():
    class PushNotifier(Notifier):
        def send(self, message):
            return f"Push: {message}"

    notifier = PushNotifier()
    service = NotificationService(notifier)

    result = notifier.send("Hi")

    assert result == "Push: Hi"