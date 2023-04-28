from abc import ABC, abstractmethod

from infrastructure.notifications.INotifier import *
from domain.SNSEventDTO import SNSEventDTO


class TestNotifier(INotifier):
    def send_message(self, message: SNSEventDTO):
        print(f"Sending message: {message}")
