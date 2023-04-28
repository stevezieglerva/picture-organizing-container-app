from abc import ABC, abstractmethod

from infrastructure.notifications.INotifier import *
from domain.SNSEventDTO import SNSEventDTO

import boto3


class SNSNotifier(INotifier):
    def send_message(self, message: SNSEventDTO):
        assert len(self.source.split(":")), f"source must be a valid AWS arn for SNS"

        print(f"Sending SNS message: {message}")

        sns = boto3.client("sns")
        result = sns.publish(
            TopicArn=self.source,
            Subject=message.subject,
            Message=str(message.message),
            MessageAttributes={
                "event_name": {"DataType": "String", "StringValue": message.name},
                "event_source": {
                    "DataType": "String",
                    "StringValue": message.source,
                },
            },
        )
        return result
