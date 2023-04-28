import json
from abc import ABC, abstractmethod

from domain.SNSEventDTO import SNSEventDTO


class INotifier(ABC):
    def __init__(self, source: str):
        self.source = source
        pass

    @abstractmethod
    def send_message(self, message: SNSEventDTO):
        raise NotImplemented
